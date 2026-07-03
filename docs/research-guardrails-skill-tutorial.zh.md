# Research Guardrails Skill 实操教程

项目地址：https://github.com/ynchen2322030451/research-guardrails-skill

适用平台：Claude Code、Codex，以及其他可以读取项目规则文件的 AI agent。

核心理念：AI 是研究副驾驶，不是数据管理员本人。AI 可以帮你整理文件、检查论文数字、写代码和做 GitHub 交接，但在删除、覆盖、同步、引用结果数字之前，必须先确认路径、备份和证据来源。

---

## 一、这个 Skill 是做什么的

`research-guardrails` 是一个通用研究安全规则包，用来降低 AI agent 在科研项目中误删数据、覆盖结果、混用证据或写出无来源结论的风险。

它主要保护四类事情：

1. 数据安全：防止 `rm -rf`、`rd /s /q`、`rsync --delete` 等危险清理命令误删数据。
2. 结果安全：防止覆盖已经冻结的模型、结果、图表和论文证据。
3. 论文安全：要求所有定量结论都能追溯到本地文件。
4. 交接安全：在 GitHub 分享前检查隐私路径、配置文件和不该公开的数据。

一句话介绍：

```text
这是一个给 AI agent 用的科研项目安全规则包，让 AI 在删改数据、跑实验、写论文数字或同步 GitHub 前，先判断风险类型，并检查路径、备份和证据来源。
```

---

## 二、安装方式

### 方式 1：下载整个仓库

```bash
git clone https://github.com/ynchen2322030451/research-guardrails-skill.git
```

然后把下面这个文件夹复制到你的项目中：

```text
.claude/skills/research-guardrails/
```

推荐项目结构：

```text
your-project/
  .claude/
    skills/
      research-guardrails/
        SKILL.md
        references/
        scripts/
        project-profile.example.yaml
```

### 方式 2：只复制 Skill 文件夹

如果不想 clone 整个仓库，也可以直接从 GitHub 下载或复制：

```text
.claude/skills/research-guardrails/
```

只要这个目录存在，Claude Code / Codex / 其他 agent 就可以读取里面的规则。

---

## 三、最简单用法

### Claude Code

如果 Claude Code 识别到了这个 skill，直接输入：

```text
/research-guardrails
```

然后继续描述你的任务。

例如：

```text
/research-guardrails
帮我清理这个项目里没用的中间文件，但不要碰原始数据和结果文件。
```

### Codex

在 Codex 中可以直接说：

```text
Use $research-guardrails. 先分类任务风险，再按规则执行。
```

例如：

```text
Use $research-guardrails. 帮我检查这个仓库能不能公开到 GitHub，重点看数据、隐私文件和结果文件。
```

### 其他 AI agent

如果某个 AI 不支持 skill，也可以把这句话贴给它：

```text
请遵守 research-guardrails 规则。先判断本次任务属于 text-only、plotting-only、postprocessing-only、experiment-changing 还是 destructive-risk；涉及删除、覆盖、同步、清理、服务器操作、GitHub 发布或论文数字时，必须先检查路径、备份和证据来源。
```

并要求它读取：

```text
.claude/skills/research-guardrails/SKILL.md
```

---

## 四、五种任务风险分类

AI 开始工作前，必须先判断当前任务属于哪一类：

| 类型 | 含义 | 是否高风险 |
|---|---|---|
| text-only | 只改文字、说明、论文表述 | 低 |
| plotting-only | 只用已有数据重新画图 | 中 |
| postprocessing-only | 只从已有 CSV/JSON/NPZ 汇总结果 | 中 |
| experiment-changing | 训练、重跑实验、生成新科学结果 | 高 |
| destructive-risk | 删除、移动、覆盖、同步删除、改权限、服务器清理 | 最高 |

如果 AI 不确定任务类型，必须按 `destructive-risk` 处理。

---

## 五、推荐默认设置

这个 skill 不要求一开始填写很多配置。默认规则已经足够保守：

- 默认保护：`data/`、`datasets/`、`raw/`、`results/`、`outputs/`、`models/`、`checkpoints/`、`figures/`、`manuscript/`、`paper/`
- 默认删除策略：不要永久删除，先移动到隔离区
- 默认论文规则：所有数字必须能追溯到本地文件
- 默认 GitHub 规则：不要上传 `.env`、`.ssh/`、`secrets/`、`private/`、`confidential/`

如果确实需要配置，只让 AI 问三件事：

```text
请先用默认设置，只向我核实三项：
1. 哪些目录是不可丢失数据？
2. 哪个结果目录或文件是当前权威版本？
3. 哪些私密目录不能上传？
```

也可以运行轻量设置脚本：

```bash
cd .claude/skills/research-guardrails
python scripts/init_project_profile.py
```

这个脚本只问三项，其他都使用推荐默认值。

---

## 六、删除或清理前怎么用

凡是涉及删除、清理、覆盖、同步删除，都先让 AI 检查命令：

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py '<要执行的命令>'
```

例子：

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py 'rm -rf $TARGET/*'
```

如果输出 `BLOCK`，就不能执行。必须改成：

1. 先 dry-run 或打印文件列表；
2. 使用绝对路径；
3. 确认备份或 GitHub 远端；
4. 优先移动到隔离区，而不是永久删除。

---

## 七、GitHub 发布前怎么用

可以直接对 AI 说：

```text
Use $research-guardrails. 帮我检查这个项目是否适合公开到 GitHub。请列出已经被 Git 跟踪的论文、数据、结果、隐私配置和大文件，并判断哪些不能公开。
```

AI 应该重点检查：

- `.env`、`.ssh/`、token、私钥、密码；
- `settings.local.json` 这类本机配置；
- 原始数据、训练数据、实验结果；
- 论文草稿、投稿文件、审稿意见；
- PPT、Word、PDF、压缩包；
- 私人路径、服务器 IP、邮箱、未公开项目材料。

重要提醒：不要把完整科研项目仓库直接改成 public。更安全的做法是新建一个干净仓库，只放可公开的工具、说明和示例。

---

## 八、常用提示词模板

### 1. 安全清理文件

```text
Use $research-guardrails. 我想清理项目里的中间文件。请先判断风险类型，列出将受影响的绝对路径，只做 dry-run，不要直接删除。
```

### 2. 检查论文数字

```text
Use $research-guardrails. 请检查这段论文表述里的每个数字是否都有本地文件支撑；没有证据的地方标记为待核实。
```

### 3. 检查能否公开 GitHub

```text
Use $research-guardrails. 请审计当前仓库是否适合公开，重点检查已被 Git 跟踪的敏感文件、数据文件、论文文件和本机配置。
```

### 4. 配置新项目

```text
Use $research-guardrails. 请使用默认设置，只向我核实三项：不可丢失数据目录、当前权威结果目录、不能上传的私密目录。
```

### 5. 数据丢失后盘点

```text
Use $research-guardrails. 我的服务器数据丢失了，请先只读盘点本地、Git 和远端还保留哪些材料，再判断哪些必须恢复、哪些可以由现有结果支撑。
```

---

## 九、适合在组会里怎么介绍

可以用下面这段话：

```text
我把一次数据事故后的经验整理成了一个通用 AI agent 安全规则包，叫 research-guardrails。它不是做实验的工具，而是一个给 Claude Code、Codex 或其他 AI 使用的安全刹车：任何删除、覆盖、同步、论文数字引用或 GitHub 发布前，AI 都要先判断风险、确认路径和备份，并把论文结论绑定到具体证据文件。大家可以从 GitHub 下载后放进自己的项目里使用。
```

GitHub 链接：

```text
https://github.com/ynchen2322030451/research-guardrails-skill
```

---

## 十、使用边界

这个 skill 不能保证绝对安全，也不能替代人工判断。它的作用是让 AI agent 在高风险操作前停下来，先做路径、备份、证据和公开性检查。

最终原则：

```text
AI 可以帮忙执行，但不能替你决定哪些数据可以删、哪些结果可以覆盖、哪些材料可以公开。
```
