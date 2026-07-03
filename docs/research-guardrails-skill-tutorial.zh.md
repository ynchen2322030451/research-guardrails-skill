# Research Guardrails Skill 实操教程

项目地址：https://github.com/ynchen2322030451/research-guardrails-skill

适用平台：Claude Code、Codex、其他可读取项目规则文件的 AI agent

版本：v1.0（2026-07-03）

---

## 一、安装方式

### Claude Code / Codex 项目内使用

进入自己的项目目录，把仓库里的 skill 文件夹复制进去：

```text
.claude/skills/research-guardrails/
```

推荐结构如下：

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

可以直接 clone：

```bash
git clone https://github.com/ynchen2322030451/research-guardrails-skill.git
```

也可以只下载 `.claude/skills/research-guardrails/` 这个目录。

---

## 二、调用方式

### Claude Code

```text
/research-guardrails
```

后面接具体任务，例如：

```text
/research-guardrails
帮我检查这个项目能不能公开到 GitHub。
```

### Codex

```text
Use $research-guardrails. 先分类任务风险，再按规则执行。
```

例如：

```text
Use $research-guardrails. 帮我清理中间文件，但不要删除原始数据、结果文件和论文材料。
```

### 其他 AI agent

如果不支持 skill 调用，让它读取：

```text
.claude/skills/research-guardrails/SKILL.md
```

并给它这段要求：

```text
请遵守 research-guardrails 规则。涉及删除、覆盖、同步、服务器操作、GitHub 发布或论文数字时，先检查路径、备份和证据来源。
```

---

## 三、它主要管什么

这个 skill 不是写论文插件，也不是实验流水线。它主要管高风险操作：

| 场景 | 作用 |
|---|---|
| 删除 / 清理文件 | 先列路径、先 dry-run，阻止递归强删 |
| 覆盖结果 | 防止覆盖已冻结的模型、数据、图表和结果 |
| 论文数字 | 要求数字能追溯到本地文件 |
| GitHub 发布 | 检查隐私文件、数据文件、本机配置和大文件 |
| 数据丢失后盘点 | 先只读盘点本地、Git、远端还剩什么 |

---

## 四、风险分类

AI 开始前会先把任务分成下面几类：

| 类型 | 说明 |
|---|---|
| text-only | 只改文字 |
| plotting-only | 只用已有数据画图 |
| postprocessing-only | 只汇总已有结果 |
| experiment-changing | 会产生新实验结果 |
| destructive-risk | 删除、移动、覆盖、同步删除、改权限、服务器清理 |

不确定时按 `destructive-risk` 处理。

---

## 五、项目配置

一般不用先配置。默认保护这些目录：

```text
data/
datasets/
raw/
results/
outputs/
models/
checkpoints/
figures/
manuscript/
paper/
```

如果新项目需要配置，只问三项：

```text
请先用默认设置，只向我核实三项：
1. 哪些目录是不可丢失数据？
2. 哪个结果目录或文件是当前权威版本？
3. 哪些私密目录不能上传？
```

也可以运行：

```bash
cd .claude/skills/research-guardrails
python scripts/init_project_profile.py
```

脚本会生成：

```text
project-profile.yaml
```

通常只需要检查这三个字段：

```yaml
protected_paths:
authoritative_results:
never_upload:
```

---

## 六、删除或清理前

先检查命令：

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py '<要执行的命令>'
```

例子：

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py 'rm -rf $TARGET/*'
```

如果输出 `BLOCK`，不要执行。

常见会被拦住的命令：

```text
rm -rf ...
find ... -delete
find ... -exec rm ...
rsync --delete
Remove-Item -Recurse
cmd /c rd /s /q ...
git clean -fdx
```

推荐替代方式：

```text
先打印文件列表
使用绝对路径
确认备份或远端
移动到 quarantine / trash，而不是永久删除
```

---

## 七、GitHub 发布前

可以这样问：

```text
Use $research-guardrails. 帮我检查这个仓库是否适合公开到 GitHub，重点看已经被 Git 跟踪的敏感文件、数据文件、论文文件和本机配置。
```

重点检查：

```text
.env
.ssh/
token / key / password
settings.local.json
原始数据
实验结果
论文草稿
审稿意见
PPT / Word / PDF
压缩包
私人路径、服务器 IP、邮箱
```

如果只是想发布一个工具，建议新建干净仓库，不要把完整科研项目仓库直接改成 public。

---

## 八、常用示例

### 清理文件

```text
Use $research-guardrails. 我想清理项目里的中间文件。请先列出将受影响的绝对路径，只做 dry-run，不要直接删除。
```

### 检查论文数字

```text
Use $research-guardrails. 请检查这段论文表述里的数字是否都有本地文件支撑；没有证据的地方标记为待核实。
```

### 检查 GitHub 可公开性

```text
Use $research-guardrails. 请审计当前仓库是否适合公开，重点检查已被 Git 跟踪的敏感文件、数据文件、论文文件和本机配置。
```

### 数据丢失后盘点

```text
Use $research-guardrails. 我的服务器数据丢失了，请先只读盘点本地、Git 和远端还保留哪些材料，再判断哪些必须恢复。
```

---

## 九、组会说明版本

可以这样介绍：

```text
这个仓库是一个通用 AI agent 安全规则包，主要用于科研项目里的数据保护、结果证据检查和 GitHub 发布前审计。使用时把 .claude/skills/research-guardrails/ 放进项目里，Claude Code 调 /research-guardrails，Codex 说 Use $research-guardrails。它不会替代人工判断，但会在删除、覆盖、同步、引用论文数字之前先做风险检查。
```

GitHub：

```text
https://github.com/ynchen2322030451/research-guardrails-skill
```

---

## 十、注意事项

- 不要让 AI 直接永久删除科研数据。
- 不要覆盖冻结结果，除非明确给新目录或新 run tag。
- 不要把论文数字写成结论，除非能指到具体文件。
- 不要把完整科研项目仓库直接公开。
- 不要上传本机配置、密钥、私有数据或未公开论文材料。
