# Research Guardrails 使用说明

这是给 AI agent 使用的通用研究安全规则包，用来约束项目中的删改数据、恢复数据、论文结果引用、图表生成和 GitHub 交接。它的目标不是替你做实验，而是让 Claude Code、Codex 或其他 AI 在动手前先检查：会不会误删数据、覆盖结果、混用证据，或者写出没有文件支撑的论文结论。

## 最简单用法

给 AI 的一句话命令：

```text
请使用 research-guardrails 规则。先判断本次任务属于 text-only、plotting-only、postprocessing-only、experiment-changing 还是 destructive-risk，再继续；涉及删除、覆盖、同步、清理或论文数字时必须先做安全和证据检查。
```

如果是 Claude Code 已安装为 skill，可以直接调用：

```text
/research-guardrails
```

如果是 Codex 或其他支持 `$skill` 触发的 agent，也可以说：

```text
Use $research-guardrails. 先分类任务风险，再按规则执行。
```

## 最方便安装方式

在你要使用的项目里，直接对 AI 说：

```text
请从 https://github.com/ynchen2322030451/research-guardrails-skill 下载 research-guardrails skill，并安装到当前项目的 .claude/skills/research-guardrails/。安装前请先检查目标目录是否已存在；如果存在，不要覆盖，先问我。安装后请告诉我 Claude Code 和 Codex 分别怎么调用。
```

安装完成后：

```text
Claude Code：/research-guardrails
Codex：Use $research-guardrails. 先分类任务风险，再按规则执行。
```

## 推荐默认设置

一般不需要先填复杂配置。默认受保护目录和私密目录清单以 `references/configuration.md` 为准；默认用“移动到隔离区”替代永久删除；默认要求论文数字必须能追溯到本地文件。

如果需要配置，只让 AI 向用户核实三件事：

```text
请先用默认设置，只向我核实三项：哪些目录是不可丢失数据？哪个结果目录/文件是当前权威版本？哪些私密目录不能上传？
```

也可以运行一个很轻量的设置脚本：

```bash
cd .claude/skills/research-guardrails
python scripts/init_project_profile.py
```

它只问这三项，其他全部使用推荐默认值。

## 删除或清理前

让 AI 先检查命令：

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py '<要执行的命令>'
```

只要出现 `BLOCK`，就不能执行，必须改成 dry-run、列出绝对路径和受影响文件，优先移动到隔离目录而不是永久删除。

## 兼容性

- Claude Code：可以作为 `.claude/skills/research-guardrails/` skill 使用，直接输入 `/research-guardrails`。
- Codex：可以说 `Use $research-guardrails`，也可以读取同一目录下的 `SKILL.md`、`references/` 和 `scripts/` 使用。
- 其他 AI agent：即使不支持 skill，也可以把上面的“一句话命令”贴给它，并要求它读取 `SKILL.md` 和相关 reference 文件。
 
核心原则：AI 只能在证据清楚、路径清楚、备份清楚、风险分类清楚之后行动。
