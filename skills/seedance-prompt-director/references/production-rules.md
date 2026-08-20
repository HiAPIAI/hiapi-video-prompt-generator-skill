# Production Rules

## Contents

1. Timing and shot budget
2. Dialogue budget
3. Action and camera feasibility
4. Continuity
5. Text and sound

## Timing and shot budget

These are production heuristics, not platform limits:

- 4-6s: 1-2 shots and one narrative beat.
- 7-10s: 2-3 shots and up to two narrative beats.
- 11-15s: 3-5 shots and up to three narrative beats.
- A literal second-by-second plan uses contiguous rows no longer than one second.
- A one-take uses one shot. Split it into timed phases while keeping a continuous camera path.

Prefer one primary physical action per shot. Preparation, execution, reaction, and recovery are separate phases when the action is complex. Do not compress a location change, costume change, fight exchange, dialogue response, and product reveal into the same two-second window.

## Dialogue budget

Use these conservative planning heuristics and revise for performance style:

- Mandarin: target 3-4 Chinese characters per second of speaking time; warn above 4.5.
- English: target 2-2.5 words per second; warn above 3.
- Leave 0.3-0.6s around emotional reactions, speaker changes, or a reveal.
- Do not place two speakers' full lines in the same second unless deliberate overlap is essential.

Count only the spoken line, not the speaker label or direction. Treat chanting, shouting, crying, and product disclaimers as slower than neutral speech.

## Action and camera feasibility

Avoid instructions that fight each other in the same time range:

| Conflict | Repair |
|---|---|
| static/locked camera + push, pan, orbit, follow | choose one, or place them in consecutive ranges |
| one-take + hard cut, montage, cutaway | remove cuts or change mode |
| slow motion + many sequential actions | reduce actions or extend duration |
| exact reference action + contradictory new blocking | state which aspect has priority |
| first-frame lock + immediate unrelated composition | add a motivated transition |
| readable text + fast camera movement | hold the frame for the text |

When referencing a video, separate what to copy: `action choreography`, `camera path`, `cut rhythm`, `transition`, or `audio`. Avoid “copy everything.”

## Continuity

For every shot or generated clip, define an end state that can be observed:

- subject position and orientation
- pose/action phase
- camera position and direction
- dominant lighting and scene state
- held prop or product orientation
- final sound or musical beat

For multi-clip work, the next clip must begin from the same observable state. Reuse the previous generated clip as the extension reference when the UI supports it. Do not assume a text description alone will preserve identity and staging.

## Text and sound

- Keep important on-screen text short and reserve a stable shot for it. Expect spelling to require post-production.
- Separate dialogue, ambience, Foley, BGM, and deliberate silence.
- Name synchronization targets: footsteps to beats, cut on impact, reveal on downbeat, or voice timbre from a reference.
- Do not ask both to preserve reference audio exactly and replace it with unrelated generated dialogue without stating priority.
