from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_plan import validate  # noqa: E402


def valid_plan() -> dict:
    return {
        "mode": "multimodal_reference",
        "duration_seconds": 4,
        "second_by_second": True,
        "one_take": False,
        "assets": [{"id": "@图片1", "type": "image", "role": "产品外观"}],
        "beats": [
            {
                "start": second,
                "end": second + 1,
                "action": "产品缓慢转动",
                "camera": "固定机位特写",
                "dialogue": "",
                "audio": "环境声",
                "refs": ["@图片1"],
            }
            for second in range(4)
        ],
    }


class ValidatePlanTests(unittest.TestCase):
    def test_valid_plan(self) -> None:
        errors, warnings = validate(valid_plan())
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_timeline_gap_and_bad_granularity(self) -> None:
        plan = valid_plan()
        plan["beats"][1]["start"] = 1.5
        errors, _ = validate(plan)
        self.assertTrue(any("gap" in message for message in errors))
        self.assertTrue(any("exactly one second" in message for message in errors))

    def test_asset_limits_and_unknown_reference(self) -> None:
        plan = valid_plan()
        plan["assets"] = [
            {"id": f"@图片{index}", "type": "image", "role": "参考"}
            for index in range(1, 11)
        ]
        plan["beats"][0]["refs"] = ["@视频1"]
        errors, _ = validate(plan)
        self.assertTrue(any("image count" in message for message in errors))
        self.assertTrue(any("undefined asset" in message for message in errors))

    def test_camera_and_one_take_conflicts(self) -> None:
        plan = valid_plan()
        plan["one_take"] = True
        plan["beats"][0]["camera"] = "固定镜头随后环绕"
        plan["beats"][1]["action"] = "硬切到产品背面"
        errors, _ = validate(plan)
        self.assertTrue(any("static camera" in message for message in errors))
        self.assertTrue(any("one_take" in message for message in errors))

    def test_dialogue_and_resolution_warnings(self) -> None:
        plan = valid_plan()
        plan["beats"][0]["dialogue"] = "这是一句明显无法在一秒钟内自然说完的中文广告台词"
        plan["dialogue_lines"] = [
            {
                "speaker": "旁白",
                "text": "这是一句明显无法在一秒钟内自然说完的中文广告台词",
                "start": 0,
                "end": 1,
            }
        ]
        plan["actual_output_resolution"] = "3840x2160"
        errors, warnings = validate(plan)
        self.assertEqual([], errors)
        self.assertTrue(any("Mandarin dialogue" in message for message in warnings))
        self.assertTrue(any("output_resolution" in message for message in warnings))

    def test_dialogue_requires_complete_line_timing(self) -> None:
        plan = valid_plan()
        plan["beats"][0]["dialogue"] = "一句台词"
        errors, _ = validate(plan)
        self.assertTrue(any("dialogue_lines is required" in message for message in errors))

    def test_continuity_anchor_required(self) -> None:
        plan = valid_plan()
        plan["requires_next_clip"] = True
        errors, _ = validate(plan)
        self.assertTrue(any("continuity_anchor" in message for message in errors))


if __name__ == "__main__":
    unittest.main()
