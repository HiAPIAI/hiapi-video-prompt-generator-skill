# HiAPI Handoff

This skill hands the final prompt to one of two HiAPI skills. This reference defines how to pick the target, how to fill the command, and what to do when the constraints conflict.

## Pick The Target Model

| Use Seedance 2.0 when | Use HappyHorse 1.0 when |
| --- | --- |
| The video is image-to-video | The video is text-to-video and the user wants a fast draft |
| Duration is `4` seconds, image-to-video, or cinematic motion control | Duration is `3`, `5`, or `15` and text-to-video draft speed matters |
| The user wants cinematic quality | The user wants throughput, not finish |
| The user mentioned Seedance | The user mentioned HappyHorse |

Default to Seedance 2.0 when the brief is ambiguous and quality matters more than speed.

## Seedance 2.0 Constraints

- **Durations** (`--seconds`): any integer from `4` to `15`.
- **Resolutions** (`--resolution`): `480p`, `720p`.
- **Aspect flag**: `--ratio`, one of `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`.
- **Image-to-video**: pass a public image URL or a data URI through `--input-reference`.

Reject the brief or adjust the defaults if the user asks for `30` seconds, `4K`, or a ratio outside the list.

## HappyHorse 1.0 Constraints

- **Durations** (`--seconds`): `3`, `5`, `8`, `10`, `15`. No other values.
- **Resolutions** (`--resolution`): `720p`, `1080p`. Do not produce a `480p` handoff for this model.
- **Aspect flag**: `--size` (not `--ratio`), one of `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. No `21:9`.
- **Input**: text-to-video only. No `--input-reference`.

HappyHorse 1.0 is the lightweight text-to-video draft model. Keep the Output Contract's scene block format, but treat each block as a macro beat rather than a tight micro cut — three to four short beats at 5 s, four to six at 10–15 s. Reserve six-scene fine cutting for Seedance 2.0.

## Handoff Command Templates

The Handoff Command in the output should be ready to paste. The `node scripts/...` line must be run **from inside the installed target skill directory**, because the scripts live there, not in this skill. Always prefix with `cd` so the user can copy both lines.

### Seedance 2.0 — Text-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video-skill" \
  || cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video" \
  || cd "$HOME/.claude/skills/hiapi-seedance-2-0-video"
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --seconds <4-15> \
  --resolution <480p|720p> \
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9>
```

### Seedance 2.0 — Image-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video-skill" \
  || cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video" \
  || cd "$HOME/.claude/skills/hiapi-seedance-2-0-video"
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --input-reference "<https-or-data-uri>" \
  --seconds <4-15> \
  --resolution <480p|720p> \
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9>
```

### HappyHorse 1.0 — Text-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-happyhorse-1-0-video" \
  || cd "$HOME/.claude/skills/hiapi-happyhorse-1-0-video"
node scripts/hiapi-happyhorse-1-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --seconds <3|5|8|10|15> \
  --resolution <720p|1080p> \
  --size <16:9|9:16|1:1|4:3|3:4>
```

Refer to the target skill's own SKILL.md for any additional flags it supports.

## What To Do When Constraints Conflict

| Conflict | Resolution |
| --- | --- |
| User wants `30` seconds | Offer the closest supported duration for the chosen target — `10` for Seedance 2.0, `15` for HappyHorse 1.0 — and a shorter scene plan. Note the change in the output. |
| User wants `4K` | Offer the target's max (`720p` for Seedance, `1080p` for HappyHorse) and explain the limit. |
| User wants a square ratio for cinematic work | Offer `1:1`, but also offer `16:9` as an alternative. |
| User wants `21:9` on HappyHorse | Either switch the target to Seedance 2.0 or downgrade to `16:9`. Do not emit `21:9` for HappyHorse. |
| User wants image-to-video with HappyHorse | Switch to Seedance 2.0. Note the switch. |
| User asks for a feature the source does not support | Drop the feature from on-screen text. Move it to Negative Constraints. |

## After Handoff

When the user runs the generated command:

- A successful Seedance 2.0 task downloads to `outputs/` when possible, or returns a remote URL.
- HappyHorse 1.0 follows the same shape but with shorter total run time.
- If the user reports an error, follow the Error Guidance section in the target skill's SKILL.md.
