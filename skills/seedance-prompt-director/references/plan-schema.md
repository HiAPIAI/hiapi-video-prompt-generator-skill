# Validation Plan Schema

Create this JSON only for complex plans that benefit from deterministic validation. It is an internal planning artifact; present the Markdown storyboard and paste-ready prompt to the user.

```json
{
  "mode": "multimodal_reference",
  "duration_seconds": 8,
  "second_by_second": true,
  "one_take": false,
  "actual_output_resolution": "834x1112",
  "assets": [
    {"id": "@Image1", "type": "image", "role": "product appearance"}
  ],
  "dialogue_lines": [
    {"speaker": "Narrator", "text": "Built for the next step.", "start": 1, "end": 3}
  ],
  "beats": [
    {
      "start": 0,
      "end": 1,
      "action": "The shoe is still on a pedestal",
      "camera": "locked close-up",
      "dialogue": "",
      "audio": "low room tone",
      "refs": ["@Image1"]
    }
  ],
  "continuity_anchor": "Shoe front-facing; camera centered; highlight held"
}
```

Required fields: `mode`, `duration_seconds`, `assets`, and `beats`. Add `dialogue_lines` whenever any dialogue is spoken; each item contains the full uninterrupted line and its actual start/end time even if the storyboard displays it across several rows. Use `second_by_second: true` for literal one-row-per-second output. Use the exact asset IDs that will appear in the prompt. For multi-clip work, validate each generated clip as a separate plan and require a nonempty `continuity_anchor` on every clip except the final one.
