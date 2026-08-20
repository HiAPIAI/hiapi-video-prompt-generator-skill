# HiAPI Seedance 提示词导演 Skill

[English](README.md)

![HiAPI Seedance 提示词导演封面](assets/cover.png)

一个把视频创意和参考素材整理成即梦 Seedance 2.0 可执行制作方案的 [Agent Skill](https://agentskills.io)。默认输出素材映射、完整逐秒分镜、可直接复制的提示词和可行性检查。

## 简介

HiAPI Seedance 提示词导演是视频生成前的制作规划层。它会整理创意需求，为每张图片、视频和音频参考指定明确用途，按照可用时长分配角色动作与运镜，并在消耗额度前校验完整方案。支持文生视频、多模态参考、首尾帧控制、视频延长、定向编辑、动作或运镜复刻、对白与声音设计，以及多片段连续性规划。

当平台安全审核拒绝原提示词时，本 Skill 也能在保留创意核心的前提下调整措辞。它不会静默提交付费生成任务；真正生成仍需独立的浏览器或 API 工具，并获得用户明确授权。

## 本版增强

- 分析可观察的素材内容；无法读取时明确标为“未核验”
- 为每个 `@图片`、`@视频`、`@音频` 指定清晰用途
- 强制输出逐秒动作、景别、运镜、对白和音效
- 校验镜头数量、物理动作和对白语速是否适合目标时长
- 检查固定机位、一镜到底、素材引用和连续性冲突
- 将超过 15 秒的目标拆成带衔接锚点的连续片段
- 将带核验日期的平台事实与“4K质感”等创作词分开
- 提供带单元测试的 JSON 制作方案校验器

本 Skill 只负责策划和提示词。只有存在独立的浏览器或 API Skill，且用户确认消耗积分后，才应提交生成任务。

## 安装

### Skills CLI

```bash
npx skills add HiAPIAI/hiapi-seedance-prompt-director-skill
```

### 手动安装

把整个仓库目录复制到 Agent 使用的 skills 目录。根目录 `SKILL.md` 是标准入口；`zh/` 下提供中文入口和中文参考资料。

## 校验

校验 Skill 结构：

macOS、Linux 或已启用 Python UTF-8 模式的环境：

```bash
python /path/to/skill-creator/scripts/quick_validate.py .
```

Windows 默认代码页可能是 GBK，直接运行上述命令会在读取 UTF-8 编码的 `SKILL.md` 时触发 `UnicodeDecodeError`。请显式启用 Python UTF-8 模式：

```powershell
python -X utf8 C:/path/to/skill-creator/scripts/quick_validate.py .
```

也可以在当前 PowerShell 会话中启用 UTF-8 模式，再运行普通校验命令：

```powershell
$env:PYTHONUTF8 = "1"
python C:/path/to/skill-creator/scripts/quick_validate.py .
```

运行制作方案校验器测试：

```bash
python -m unittest discover -s tests -v
python scripts/validate_plan.py plan.json
```

## 资料来源

平台参数来自[即梦 Seedance 2.0 官方使用手册](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ)，核验日期记录在 `zh/references/platform-constraints.md`。即梦可能独立更新，实际消耗积分前仍以账号当前界面为准。

工作流设计还对比了 [songguoxs/seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill) 的长视频衔接方式，以及 [AKCodez/higgsfield-claude-skills](https://github.com/AKCodez/higgsfield-claude-skills) 对“提示词设计”和“消耗积分的浏览器自动化”的职责拆分。本仓库没有引入外部自动化代码。

## 许可证

[MIT](LICENSE)
