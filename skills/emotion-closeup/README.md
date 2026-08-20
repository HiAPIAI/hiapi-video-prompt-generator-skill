# Emotion Close-up Prompt

**[English](#english) · [中文](#中文)**

<a id="english"></a>

A Claude Code / Codex CLI skill for writing hyper-realistic **emotional close-up performance prompts** for AI video models (Sora, Veo, Kling, Jimeng, Hailuo, …) — crying scenes, suppressed feelings, quiet breakdowns, bittersweet micro-expressions.

## The core idea

Video models can't act abstract emotions — they render **time-ordered physical events**. So this skill never writes "he is devastated". It writes *which muscle moves, in which direction, at what amplitude, for how long, and which muscle takes over next*. Realism comes from **resistance, not intensity**: the quality of a breakdown is decided by the quality of the suppression before it.

## The six-stage emotional arc

| # | Stage | What happens |
|---|-------|--------------|
| 1 | Absorb | The event lands: hollow gaze, unfocused eyes, a restrained swallow, lips part then close — nothing comes out |
| 2 | Suppress | Full muscle mobilization (pressed lips, brow, orbicularis oculi); the first physiological leak is forced back (tear line → rapid blinking → reddened corners) |
| 3 | The crack | A 2–3s **mixed micro-expression** — brow still sad while the mouth almost smiles — noticed by the character and actively re-suppressed |
| 4 | Failed self-rescue | A physically motivated move backfires: head tilts up to use gravity against the tears → one uncontrollable blink → first tear overflows (right eye first, left eye later) |
| 5 | Overflow | Quiet surrender: tear tracks catching the side light, no more blinking them away |
| 6 | Takeover | The body overrules the will: trembling lower lip, shattered breathing, the first involuntary sound, irregular shoulder tremors — no theatrics |

**Five realism principles:** name muscles instead of emotions · every movement carries an amplitude adverb · give emotion a physical opponent (gravity, blinks, light) · break symmetry · write the body-vs-will gap.

Swap the emotion, keep the arc: suppressed laughter, held-back anger, tears of joy, masked fear, being disarmed by kindness — see `references/emotion-library.md`.

## Repo structure

```
├── SKILL.md                        ← method + workflow + QC checklist (skill entry point)
├── references/
│   ├── emotion-library.md          ← 7 emotion recipes + the canonical crying prompt, line-by-line annotated
│   └── anatomy-physics.md          ← muscle map, tear physics, breathing/sound vocabulary, amplitude adverbs
└── templates/
    └── prompt-template.md          ← fill-in-the-blank prompt template
```

## Install

```bash
git clone https://github.com/HiAPIAI/hiapi-emotion-closeup.git

# Claude Code
cp -r hiapi-emotion-closeup ~/.claude/skills/emotion-closeup-prompt

# Codex CLI
cp -r hiapi-emotion-closeup ~/.codex/skills/emotion-closeup-prompt
```

Restart the agent. No tokens, no dependencies.

## Usage

Just ask in natural language:

| You say | You get |
|---|---|
| "Write a crying-scene close-up prompt" | Full six-stage prompt, ready to paste into the video model |
| "Tears of joy / suppressed laughter / held-back anger" | Same arc, swapped emotion recipe |
| "Only 8 seconds" | Compressed three-stage version (suppress → crack → overflow) |
| "The face distorted / the acting was too much" | Local revision: lower amplitude adverbs, add anatomical anchors — never a rewrite |

**Production note:** a full six-stage arc is ≈20–30s. For single generations (5–10s), split into clips (stages 1+2 / 3+4 / 5+6) or use the compressed version.

---

<a id="中文"></a>

# 人物情绪特写 Prompt Skill

给 AI 视频模型（Sora / Veo / 可灵 / 即梦 / Hailuo 等）写**人物情绪特写表演 prompt** 的 Claude Code / Codex 技能——哭戏、强忍、破防、微表情、喜极而泣、愤怒克制。

## 核心原理

视频模型不会演抽象情绪，只会演**带时间顺序的物理事件**。所以不写「他很悲伤」，写「哪块肌肉、往哪动、多大幅度、持续几秒、接下来哪块肌肉接管」。真实感来自**抵抗**而非强度——崩溃的质量取决于前面压制的质量。

## 六阶段情绪弧线

**承接**（空洞失焦、克制的吞咽、欲言又止）→ **压制**（肌群总动员，第一波泪水被密集眨眼压回）→ **裂缝**（2-3 秒混合微表情：眉头皱着+嘴角上扬，被本人察觉后主动收敛）→ **自救失败**（仰头借重力逼泪，反被一次不受控的眨眼击溃，右眼先流左眼稍晚）→ **溢出**（泪痕在侧光下反光，不再抵抗）→ **接管**（唇颤、呼吸碎裂、第一个不由自主的声音、肩膀细碎颤动，没有戏剧感）

**五条真实感原则：** 肌肉命名代替情绪词 · 每个动作带幅度副词 · 给情绪一个物理对手（重力/眨眼/光）· 对称破缺 · 身体与意志的 Gap。

换情绪不换结构：强忍笑意、愤怒克制、喜极而泣、强装镇定、被温柔击穿的委屈——配方见 `references/emotion-library.md`。

## 目录结构

```
├── SKILL.md                        ← 方法论 + 工作流 + 自检清单（skill 入口）
├── references/
│   ├── emotion-library.md          ← 7 种情绪配方 + 基准哭戏 prompt 全文逐句标注
│   └── anatomy-physics.md          ← 肌肉速查、泪水物理链、呼吸/声音词汇、幅度副词阶梯
└── templates/
    └── prompt-template.md          ← 可直接填空的 prompt 模板
```

## 安装

```bash
git clone https://github.com/HiAPIAI/hiapi-emotion-closeup.git

# Claude Code
cp -r hiapi-emotion-closeup ~/.claude/skills/emotion-closeup-prompt

# Codex CLI
cp -r hiapi-emotion-closeup ~/.codex/skills/emotion-closeup-prompt
```

重启 agent 即可。无 token、无依赖。

## 用法

自然语言直接说：

| 你说的话 | 拿到什么 |
|---|---|
| 「写一段哭戏的情绪特写 prompt」 | 完整六阶段 prompt，可直接投喂视频模型 |
| 「喜极而泣 / 强忍笑意 / 愤怒克制」 | 弧线不变，换情绪配方 |
| 「只有 8 秒」 | 三段压缩版（压制→裂缝→溢出） |
| 「出片脸崩了 / 演太过了」 | 局部修订：降幅度副词、补解剖词，不重写 |

**产线提示：** 完整六阶段 ≈20–30 秒，单条生成（5–10s）放不下——按 1+2 / 3+4 / 5+6 拆条再剪，或用三段压缩版。
