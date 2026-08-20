---
name: hiapi-seedance-prompt-director
description: Design production-ready prompts and second-by-second storyboards for Jimeng Seedance 2.0 using text, image, video, and audio references. Use for Seedance or Jimeng video ideation, prompt writing, asset analysis and @reference mapping, shot planning, dialogue and sound timing, video extension or editing, and feasibility checks. This skill prepares prompts but does not submit generation jobs unless a separate browser or API tool is available and the user authorizes it.
---

# HiAPI Seedance Prompt Director

Turn a video idea and available media into a prompt that can be pasted into Jimeng. Treat platform limits as versioned facts, creative wording as guidance, and every generated shot as a time-budgeted production decision.

## Load only what is needed

- Read [references/platform-constraints.md](references/platform-constraints.md) before quoting platform limits, upload policy, output resolution, or model availability.
- Read [references/production-rules.md](references/production-rules.md) when the request includes dialogue, multiple shots, a one-take, complex action, or more than 8 seconds.
- Read [references/prompt-patterns.md](references/prompt-patterns.md) only for the matching workflow: references, extension, editing, beat sync, product, drama, or long-form continuation.
- Read [references/evaluation-cases.md](references/evaluation-cases.md) when evaluating or revising this skill.

## Operating boundary

- Produce plans, prompts, asset instructions, and validation results.
- Inspect user-provided media with available image, video, or audio tools. Report only observable facts. If media cannot be inspected, label its content and duration as unverified instead of inventing details.
- Do not claim that a video was generated or submitted. Use a separate generation/browser skill when available. Obtain confirmation immediately before an action that spends credits or publishes content.
- Never describe style terms such as `4K look` as the actual output resolution.

## Workflow

### 1. Normalize the brief

Extract the goal, duration, aspect ratio, audience/platform, visual style, required story beat, dialogue, and available assets. Do not ask for information already present. If nonessential details are absent, choose conservative defaults and state them briefly. Ask only when a missing choice would materially change the result.

Select one mode:

- text-to-video
- multimodal reference
- first/last-frame control
- video extension
- video edit or replacement
- rhythm/action/camera replication
- multi-clip sequence for a target longer than 15 seconds

### 2. Inspect and map assets

Create an asset manifest before writing the prompt:

| Asset | Verified observations | Assigned role | Reference phrase |
|---|---|---|---|
| `@Image1` | observable subject, framing, style | character / product / first frame | `Use @Image1 for...` |

Assign exactly one primary role and optional secondary roles to each asset. Distinguish identity/appearance, composition, scene, action, camera, transition, rhythm, voice, BGM, and sound effects. Do not use an asset that is not in the manifest. Do not leave an uploaded asset unassigned.

If an asset needed for continuity cannot be inspected, mark its observations unverified and request only the missing facts that block a final prompt. Do not stop there: return a conditional production scaffold with explicit `[verify: ...]` placeholders wherever the unknown source state affects action, camera, lighting, identity, or sound. A `BLOCKED` status prevents a generation-ready claim; it does not permit omitting the required sections.

### 3. Budget the video

Use one generation for 4-15 seconds. For a longer target, split it into clips of at most 15 seconds and define a concrete continuity anchor between clips.

Treat every generated clip as a separate production unit. Give each clip its own local duration, timeline starting at `0`, paste-ready or clearly conditional prompt, observable start state, final continuity anchor, next-clip reference mapping, and sound handoff. Never replace these local timelines with one combined timeline across multiple generations.

Default shot budgets:

| Duration | Recommended shots |
|---|---:|
| 4-6s | 1-2 |
| 7-10s | 2-3 |
| 11-15s | 3-5 |

A one-take has one shot with timed phases, not hidden cuts. Give each shot one primary subject action and one primary camera move; add more only when they can physically overlap. Reserve readable screen text for a held shot. Budget dialogue using the heuristics in `production-rules.md`.

### 4. Build a complete timeline

Default to a second-by-second beat sheet. Cover every second from `0` to the selected duration with no gaps or overlaps. Each row must describe:

| Time | Subject and action | Framing and camera | Dialogue / sound | Reference |
|---|---|---|---|---|

Use one row per second for explicit “second-by-second” requests. For simple motion, adjacent seconds may share an action, but each row must still state the evolving state. Do not omit table columns; use `—` when a row has no dialogue, sound, or reference. For extension, number time from `0` for the newly generated portion and separately state the source-video continuity anchor.

### 5. Write the paste-ready prompt

Order information by generation priority:

1. duration, mode, and primary subject
2. precise asset roles
3. chronological action and camera instructions
4. dialogue, ambience, Foley, BGM, and silence
5. visual treatment and exclusions

Use natural language, not a pile of adjectives. Repeat an `@reference` only when it clarifies a different role. Keep prompt complexity within the timeline budget.

### 6. Validate before delivery

Check all of the following:

- duration and continuous timeline coverage
- input counts and total-file limit against the dated platform reference
- every `@reference` exists and has a stated role
- no static-camera / moving-camera or one-take / cut conflict
- actions fit their allotted time
- dialogue fits its speaking window
- start and end states are explicit
- continuity anchors exist for multi-clip work
- actual output claims are separated from stylistic quality language
- uncertain platform rules are labeled as needing UI verification

For any plan with dialogue, more than one shot, a duration over 8 seconds, multiple references, literal second-by-second output, or a following clip, serialize the plan using [references/plan-schema.md](references/plan-schema.md) and run:

```bash
python scripts/validate_plan.py plan.json
```

Use the actual speaking window of each line, not the total video duration, when measuring dialogue rate. Fix errors before answering. Surface warnings as tradeoffs rather than silently ignoring them. The JSON plan is an internal validation artifact and does not need to be shown to the user.

## Required output contract

Unless the user explicitly asks for prompt-only output, return these sections in order:

1. **Production settings**: mode, duration, ratio, assumptions.
2. **Asset manifest**: every supplied or recommended asset and its exact role.
3. **Second-by-second storyboard**: complete timeline with action, camera, sound, and references.
4. **Seedance prompt**: one copy-ready Chinese prompt by default; use another language only when requested.
5. **Feasibility check**: `PASS`, `WARN`, or `BLOCKED` for timing, references, continuity, policy/UI uncertainty, and complexity. For every spoken line, show character/word count, its actual speaking window, and the resulting rate before assigning a status.
6. **Generation notes**: only the settings or upload order the user must apply in Jimeng.

If the brief is infeasible, do not disguise it with more adjectives. Return a conservative version that fits and identify what was deferred. `BLOCKED` is a feasibility result, not permission to omit the storyboard, prompt, or generation notes; when source facts are unavailable, keep those sections conditional and use explicit verification placeholders instead of invented details.
