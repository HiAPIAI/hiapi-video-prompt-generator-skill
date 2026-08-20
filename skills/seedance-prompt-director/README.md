# HiAPI Seedance Prompt Director Skill

[中文](README-zh.md)

![HiAPI Seedance Prompt Director cover](assets/cover.png)

An [Agent Skill](https://agentskills.io) for turning a video idea and reference media into a production-ready Jimeng Seedance 2.0 plan. It produces an asset map, a complete second-by-second storyboard, a paste-ready prompt, and a feasibility report.

## Overview

HiAPI Seedance Prompt Director is the planning layer before video generation. It normalizes a creative brief, assigns an exact role to every image, video, and audio reference, budgets actions and camera moves against the available duration, and validates the finished plan before credits are spent. It supports text-to-video, multimodal references, first/last-frame control, extensions, targeted edits, camera or action replication, dialogue timing, sound design, and multi-clip continuity.

The skill prepares production-ready prompts and can revise wording when a platform safety review rejects an otherwise valid concept. It does not silently submit paid generation jobs: generation requires a separate browser or API tool and explicit user authorization.

## What it adds

- observable media analysis with explicit “unverified” handling
- precise `@Image` / `@Video` / `@Audio` role assignment
- literal second-by-second action, camera, dialogue, and sound planning
- timing budgets for shots, physical actions, and spoken lines
- conflict checks for camera direction, one-takes, references, and continuity
- multi-clip continuation for targets longer than 15 seconds
- dated platform facts separated from creative quality language
- a deterministic JSON plan validator with unit tests

This skill prepares prompts. It does not submit a generation job unless a separate browser or API skill is available and the user authorizes the credit-spending action.

## Install

### Skills CLI

```bash
npx skills add HiAPIAI/hiapi-seedance-prompt-director-skill
```

### Manual

Copy the repository folder into the skills directory used by your agent. The canonical entry point is `SKILL.md`. A Chinese-localized entry point and references are under `zh/`.

## Validation

Validate the skill package:

On macOS, Linux, or an environment where Python UTF-8 mode is already enabled:

```bash
python /path/to/skill-creator/scripts/quick_validate.py .
```

Windows may use GBK as its default code page, causing `UnicodeDecodeError` when the validator reads the UTF-8 encoded `SKILL.md`. Explicitly enable Python UTF-8 mode:

```powershell
python -X utf8 C:/path/to/skill-creator/scripts/quick_validate.py .
```

Alternatively, enable UTF-8 mode for the current PowerShell session before running the standard validation command:

```powershell
$env:PYTHONUTF8 = "1"
python C:/path/to/skill-creator/scripts/quick_validate.py .
```

Run the deterministic plan checks:

```bash
python -m unittest discover -s tests -v
python scripts/validate_plan.py plan.json
```

## Sources

Platform facts are based on the [official Seedance 2.0 user manual](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ) and are stored with a verification date in `references/platform-constraints.md`. Because Jimeng can change independently of this repository, the current UI remains authoritative before spending credits.

The workflow design was also compared against [songguoxs/seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill) for long-form continuation patterns and [AKCodez/higgsfield-claude-skills](https://github.com/AKCodez/higgsfield-claude-skills) for the separation between prompt creation and credit-spending browser automation. No external automation code is included here.

## License

[MIT](LICENSE)
