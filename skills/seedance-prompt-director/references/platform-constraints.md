# Platform Constraints

## Source and confidence

Primary source: [Jimeng Seedance 2.0 User Manual](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ), shown as modified July 30, 2026 when checked on August 4, 2026 (Beijing time).

Use the following values as documented platform facts, but verify the current Jimeng UI before spending credits because rollout, policy, and model options can change without this repository changing.

| Item | Documented value |
|---|---|
| Images | up to 9; jpeg/png/webp/bmp/tiff/gif; each under 30 MB |
| Videos | up to 3; mp4/mov; combined reference duration 2-15s; each under 50 MB |
| Audio | up to 3; mp3/wav; combined duration up to 15s; each under 15 MB |
| Combined files | up to 12 image/video/audio files |
| Generated duration | selectable from 4-15s |
| Reference-video pixels | documented total-pixel range 409,600 to 927,408 |
| Sound | generated video can include sound effects/music |

The manual also stated that Seedance 2.0 was fully rolled out and mentioned a Seedance 2.0 Fast option. Treat model availability as UI-dependent.

## Facts versus creative language

- `cinematic`, `film grain`, `4K look`, and `high-detail CGI` are visual directions, not guaranteed export specifications.
- Do not convert the documented reference-video pixel range into a promise that generated output is a particular resolution.
- Do not promise a frame rate, codec, exact aspect ratio, lip-sync accuracy, or text-rendering accuracy unless the current UI explicitly exposes it.
- Content moderation rules can vary by region, account, source material, and rollout. Describe any current restriction only after checking the UI or a current official policy. Do not preserve the old blanket claim that every realistic human face is always rejected as an timeless model capability.

## Reference syntax

In the Chinese Jimeng UI, use the asset labels inserted by the UI, normally `@图片1`, `@视频1`, and `@音频1`. In English explanations, `@Image1`, `@Video1`, and `@Audio1` are readable aliases, but the paste-ready prompt must match the labels shown in the user's UI.

Always state the role being referenced: appearance, composition, scene, action, camera, transition, rhythm, voice, BGM, or effects.
