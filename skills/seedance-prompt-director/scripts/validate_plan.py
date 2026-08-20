#!/usr/bin/env python3
"""Validate a structured Seedance production plan before prompt delivery."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ASSET_LIMITS = {"image": 9, "video": 3, "audio": 3}
MAX_FILES = 12
EPSILON = 1e-6
STATIC_TERMS = ("static", "locked", "fixed", "固定", "锁定")
MOVING_TERMS = (
    "push",
    "pull",
    "pan",
    "tilt",
    "orbit",
    "track",
    "follow",
    "crane",
    "推镜",
    "拉镜",
    "摇镜",
    "环绕",
    "跟拍",
    "跟随",
    "升降",
)
CUT_TERMS = ("hard cut", "jump cut", "montage", "cutaway", "硬切", "跳切", "蒙太奇", "插入镜头")


def _number(value: Any, field: str, errors: list[str]) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{field} must be a number")
        return None
    return float(value)


def _contains(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def validate(plan: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(plan.get("mode"), str) or not plan["mode"].strip():
        errors.append("mode must be a non-empty string")

    duration = _number(plan.get("duration_seconds"), "duration_seconds", errors)
    if duration is not None and not 4 <= duration <= 15:
        errors.append("duration_seconds must be between 4 and 15 for each generation")

    assets = plan.get("assets")
    if not isinstance(assets, list):
        errors.append("assets must be a list")
        assets = []

    ids: set[str] = set()
    counts: Counter[str] = Counter()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"assets[{index}] must be an object")
            continue
        asset_id = asset.get("id")
        asset_type = asset.get("type")
        role = asset.get("role")
        if not isinstance(asset_id, str) or not asset_id.startswith("@"):
            errors.append(f"assets[{index}].id must be an @reference string")
        elif asset_id in ids:
            errors.append(f"duplicate asset id: {asset_id}")
        else:
            ids.add(asset_id)
        if asset_type not in ASSET_LIMITS:
            errors.append(f"assets[{index}].type must be image, video, or audio")
        else:
            counts[asset_type] += 1
        if not isinstance(role, str) or not role.strip():
            errors.append(f"assets[{index}].role must state the asset's purpose")

    for asset_type, limit in ASSET_LIMITS.items():
        if counts[asset_type] > limit:
            errors.append(f"{asset_type} count {counts[asset_type]} exceeds documented limit {limit}")
    if sum(counts.values()) > MAX_FILES:
        errors.append(f"combined asset count {sum(counts.values())} exceeds documented limit {MAX_FILES}")

    beats = plan.get("beats")
    if not isinstance(beats, list) or not beats:
        errors.append("beats must be a non-empty list")
        beats = []

    parsed_beats: list[tuple[float, float, dict[str, Any], int]] = []
    for index, beat in enumerate(beats):
        if not isinstance(beat, dict):
            errors.append(f"beats[{index}] must be an object")
            continue
        start = _number(beat.get("start"), f"beats[{index}].start", errors)
        end = _number(beat.get("end"), f"beats[{index}].end", errors)
        if start is None or end is None:
            continue
        if end <= start:
            errors.append(f"beats[{index}] must end after it starts")
        parsed_beats.append((start, end, beat, index))

        refs = beat.get("refs", [])
        if not isinstance(refs, list):
            errors.append(f"beats[{index}].refs must be a list")
        else:
            for ref in refs:
                if ref not in ids:
                    errors.append(f"beats[{index}] references undefined asset {ref}")

        camera = str(beat.get("camera", ""))
        if _contains(camera, STATIC_TERMS) and _contains(camera, MOVING_TERMS):
            errors.append(f"beats[{index}] combines a static camera with camera movement")

        if not isinstance(beat.get("action"), str) or not beat["action"].strip():
            errors.append(f"beats[{index}].action must describe the evolving subject state")
        if not isinstance(beat.get("camera"), str) or not beat["camera"].strip():
            errors.append(f"beats[{index}].camera must describe framing or camera state")

    parsed_beats.sort(key=lambda item: (item[0], item[1]))
    if parsed_beats:
        if abs(parsed_beats[0][0]) > EPSILON:
            errors.append("timeline must start at 0")
        previous_end = parsed_beats[0][1]
        for start, end, _, index in parsed_beats[1:]:
            if start > previous_end + EPSILON:
                errors.append(f"timeline gap before beats[{index}]: {previous_end:g}-{start:g}s")
            elif start < previous_end - EPSILON:
                errors.append(f"timeline overlap at beats[{index}]: starts {start:g}s before {previous_end:g}s")
            previous_end = max(previous_end, end)
        if duration is not None and abs(previous_end - duration) > EPSILON:
            errors.append(f"timeline ends at {previous_end:g}s, expected {duration:g}s")

    if plan.get("second_by_second") is True:
        for start, end, _, index in parsed_beats:
            if abs((end - start) - 1) > EPSILON:
                errors.append(f"beats[{index}] must cover exactly one second in second-by-second mode")
            if abs(start - round(start)) > EPSILON or abs(end - round(end)) > EPSILON:
                errors.append(f"beats[{index}] must use integer boundaries in second-by-second mode")

    if plan.get("one_take") is True:
        combined = " ".join(
            f"{beat.get('action', '')} {beat.get('camera', '')}" for _, _, beat, _ in parsed_beats
        )
        if _contains(combined, CUT_TERMS):
            errors.append("one_take conflicts with cut or montage instructions")

    has_dialogue = any(str(beat.get("dialogue", "")).strip(" —-") for _, _, beat, _ in parsed_beats)
    dialogue_lines = plan.get("dialogue_lines")
    if has_dialogue and not isinstance(dialogue_lines, list):
        errors.append("dialogue_lines is required when beats contain dialogue")
        dialogue_lines = []
    elif dialogue_lines is None:
        dialogue_lines = []
    elif not isinstance(dialogue_lines, list):
        errors.append("dialogue_lines must be a list")
        dialogue_lines = []

    for index, line in enumerate(dialogue_lines):
        if not isinstance(line, dict):
            errors.append(f"dialogue_lines[{index}] must be an object")
            continue
        text = line.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"dialogue_lines[{index}].text must contain the complete spoken line")
            continue
        start = _number(line.get("start"), f"dialogue_lines[{index}].start", errors)
        end = _number(line.get("end"), f"dialogue_lines[{index}].end", errors)
        if start is None or end is None:
            continue
        if end <= start:
            errors.append(f"dialogue_lines[{index}] must end after it starts")
            continue
        if start < 0 or (duration is not None and end > duration + EPSILON):
            errors.append(f"dialogue_lines[{index}] falls outside the generated duration")
        window = end - start
        chinese_chars = len(re.findall(r"[\u3400-\u9fff]", text))
        english_words = len(re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", text))
        if chinese_chars / window > 4.5:
            warnings.append(
                f"dialogue_lines[{index}] Mandarin dialogue is {chinese_chars} chars / {window:g}s "
                f"= {chinese_chars / window:.1f} chars/s; target 3-4"
            )
        if english_words / window > 3:
            warnings.append(
                f"dialogue_lines[{index}] English dialogue is {english_words} words / {window:g}s "
                f"= {english_words / window:.1f} words/s; target 2-2.5"
            )

    resolution = plan.get("actual_output_resolution")
    if isinstance(resolution, str):
        match = re.fullmatch(r"\s*(\d+)\s*[xX×]\s*(\d+)\s*", resolution)
        if not match:
            warnings.append("actual_output_resolution is not in WIDTHxHEIGHT format")
        elif int(match.group(1)) * int(match.group(2)) > 927_408:
            warnings.append(
                "actual_output_resolution exceeds the pixel range documented for reference videos; "
                "verify the current UI and do not present style terms as an export guarantee"
            )

    if plan.get("requires_next_clip") is True and not str(plan.get("continuity_anchor", "")).strip():
        errors.append("continuity_anchor is required when another generated clip follows")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to a UTF-8 JSON plan")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results")
    args = parser.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read plan: {exc}", file=sys.stderr)
        return 2
    if not isinstance(plan, dict):
        print("ERROR: plan root must be a JSON object", file=sys.stderr)
        return 2

    errors, warnings = validate(plan)
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARN: {message}")
        if not errors and not warnings:
            print("PASS: plan is valid")
        elif not errors:
            print("PASS WITH WARNINGS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
