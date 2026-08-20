# Prompt Patterns

Use placeholders and keep only the clauses supported by the plan.

## Multimodal reference

```text
[duration], full-reference mode. Use @Image1 only for [appearance/product details]; use @Image2 for [scene/composition]; use @Video1 only for [camera path/action/cut rhythm]; use @Audio1 for [BGM/voice/rhythm]. [chronological actions]. [sound]. [visual treatment]. Do not [specific exclusion].
```

## First and last frame

```text
Use @Image1 as the first frame and @Image2 as the final composition. [subject] moves from [observable start state] to [observable end state] through [one plausible action path]. Camera [movement]. Preserve [identity/product details].
```

## Extension

Number only the newly generated duration from zero.

```text
Extend @Video1 by [N] seconds. Continue from its final state: [pose, position, camera, lighting, sound]. 0-...s: [...]. End with [observable continuity anchor].
```

## Targeted edit

```text
Edit @Video1. Change only [target element] to [new state/reference], preserving [camera, timing, background, other subjects, audio]. At [time/event], [precise edit].
```

## Action or camera replication

```text
Use @Image1 for the subject's appearance. From @Video1 reference only [action choreography/camera path/rhythm], not [excluded properties]. Adapt movement to [new scene/wardrobe/prop] while preserving [start and end pose].
```

## Beat sync

```text
Use @Audio1 as the timing source. Cut or change action on [named beats/events]. Use @Image1-@ImageN for [assigned scenes]. Preserve a readable visual state between beats; do not add unassigned imagery.
```

## Product shot

Use 1-3 controlled product actions: reveal, rotation, interaction, detail, or final hold. Preserve logo geometry and product proportions. If exact typography matters, recommend adding it in post rather than promising model-rendered text.

## Dialogue scene

Give each speaker a separate time window and reaction beat. Put the line in quotes and specify performance briefly. Prefer a simple camera plan that protects lip-sync and facial continuity.

## More than 15 seconds

Split by narrative beats. For each clip provide:

1. local duration and paste-ready prompt
2. first observable state
3. final continuity anchor
4. which generated clip becomes the next `@Video1`
5. sound handoff or edit point

Reset the newly generated time to `0` in every clip; do not present one combined timeline across separate generations. If the source video is unavailable or uninspectable, keep the result `BLOCKED` but still provide every clip as a conditional scaffold. Use placeholders such as `[verify source end pose]`, `[verify camera direction]`, and `[verify sound handoff]` rather than inventing continuity facts.
