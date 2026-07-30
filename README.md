# quick-learn-everything

一个**跨 agent 通用**的学习教练 skill。装到 Claude Code、Cursor、ChatGPT、Antigravity、Codex、WorkBuddy 任意一个里，它都会用同一套十步闭环带你吃透一个领域。

> 大多数人只是随意提问，感觉在学习，一周后什么都不记得。
> 因为真正的学习需要四个要素：**一条路径，一次测试，一次压缩，一个反馈循环。**
> —— Rahul（@sairahul1）

## 方法出处

融合两套方法：

**Rahul（@sairahul1）的四要素** —— 路径、测试、压缩、反馈循环。缺一个，学习就退化成「感觉在学习」。

**STORM**（Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking），斯坦福，发表于 NAACL。论文称一份博士级调研人工要 40–60 小时读资料理线索，它用检索加多视角提问压缩到几分钟。它的核心洞察是：

> 我们大多数情况下问 AI「给我讲讲 X」，得到的永远是大多数人的观点、最常见的框架、最表面的信息。
> 可一个领域真正的样子，从来不长在大多数人的观点里。

十步流程是对两者的融合，另外补了 STORM 自己承认的短板（缺自我批判 → 第 4 步），并接上了记忆与回顾的闭环（第 8–10 步）。

## 十步

| 阶段 | 步骤 | 做什么 |
|---|---|---|
| **一 · 建图** | 1 五视角 STORM | 实践者 / 学者 / 怀疑者 / 经济学家 / 历史学家，五种人看到的根本不是同一个东西 |
| | 2 矛盾图谱 | 让五个视角互相质疑。**浅调研与深调研的分水岭** |
| | 3 综合简报 | 收拢成一份任何单一视角都写不出来的简报 |
| | 4 同行评审自检 | 让 AI 给自己挑刺，补 STORM 缺自我批判的短板 |
| **二 · 铺路** | 5 资源筛选 | **只给 5 个**，外加该躲开的坑和一周路径 |
| | 6 学习阶梯 | 5 级阶梯，依据维果茨基最近发展区，解决跳级学的问题 |
| | 7 核心 20% | 10 次课先拿下能上手干活的那部分 |
| **三 · 夯实** | 8 考到崩溃 | 10 题递进，**一次只问一道**。测试效应 |
| | 9 费曼循环 | 讲不清的地方磨平，**讲清楚前不进新内容** |
| **四 · 压缩** | 10 一页速查表 | 5 分钟扫完，上场前用 |

四要素的对应关系：**路径**=5–7，**测试**=8，**压缩**=10，**反馈循环**=9（与 4）。

**双模式自适应**：能读写文件时产出落到 `./learning/<topic>/`，跨会话续学（每次先读 `progress.md` 恢复进度）；纯对话环境则全部在对话内给出。

## 安装

### Claude Code / Claude 系

```bash
git clone https://github.com/vivilin-ai/quick-learn-everything.git
mkdir -p ~/.claude/skills/quick-learn-everything
cp -r quick-learn-everything/{SKILL.md,references} ~/.claude/skills/quick-learn-everything/
```

只想在某个项目里用就放 `<项目>/.claude/skills/` 下。之后说「我想快速入门 XX」会自动触发。

### Cursor

把 `.cursor/rules/quick-learn-everything.mdc` 拷进项目的 `.cursor/rules/`。该文件自包含（参考资料已内联），单独拷贝即可。

规则设的是 `alwaysApply: false`，靠 description 按需触发，不污染日常对话。

### Codex / Antigravity / 其他遵循 AGENTS.md 约定的 agent

把 `AGENTS.md` 放到项目根目录，已有的话追加进去。同样自包含。

### ChatGPT / WorkBuddy / 其他纯对话环境

这类环境读不到仓库文件，用 `dist/` 下的单文件版本：

- **`dist/PROMPT.md`** —— 完整版（约 24k 字符），含十步原始提示词、方法论展开和全部产出模板。粘贴到对话开头
- **`dist/PROMPT-compact.md`** —— 精简版（约 5.9k 字符）。用于 Custom GPT 的 Instructions，那里有 **8000 字符硬上限**。保留十步骨架、命门规则和防幻觉规则，裁掉产出模板

### 只想手动跑，不装 skill

`references/prompts.md` 里是**十步的原始提示词全文**，替换 `【】` 里的内容，一步一步贴给任何 AI 即可。

## 改这个 skill

**唯一的手写源是 `SKILL.md` 和 `references/`。** 其余四个文件是构建产物：

```
SKILL.md ────┐
             ├──► scripts/build.py ──► AGENTS.md
references/ ─┘                         .cursor/rules/quick-learn-everything.mdc
                                       dist/PROMPT.md
                                       dist/PROMPT-compact.md
```

```bash
python scripts/build.py          # 重新生成产物
python scripts/build.py --check  # 校验产物与源一致（不一致非零退出，可挂 CI）
```

**不要手改产物文件**——下次构建会覆盖。`--check` 就是为了在 CI 里拦住这种漂移。

构建时强制三件事：

1. `PROMPT-compact.md` 正文 ≤ 8000 字符，超了报错而不是静默截断
2. 自包含产物里不留 `references/xxx.md` 这类悬空引用（粘贴进 ChatGPT 后会指向虚空）
3. 产物里不残留 `compact:skip` / `compact:include` 构建标记

### 两个构建标记

```markdown
<!-- compact:skip -->    包裹的段落不进精简版（写在 SKILL.md 里）
<!-- compact:include --> 包裹的段落要进精简版（写在 references/ 里）
```

两种标记在所有产物中都会被剥掉，只影响内容取舍。

## 仓库结构

```
SKILL.md                    ★ 源：Agent Skills 格式，十步骨架
references/                 ★ 源：按需加载
  prompts.md                  十步原始提示词全文（权威规格）
  method.md                   每步的展开、判据、常见失败模式、方法出处
  source-quality.md           第 5 步的信源筛选标准 + 防幻觉规则
  templates/                  落盘模式的产出骨架
    research-brief.md           第 1–4 步
    resources.md                第 5 步
    learning-plan.md            第 6–7 步
    drill-log.md                第 8–9 步
    cheatsheet.md               第 10 步
    progress.md                 跨会话进度
scripts/build.py            构建 + 校验
AGENTS.md                   ⚙ 产物
.cursor/rules/*.mdc         ⚙ 产物
dist/PROMPT*.md             ⚙ 产物
```

`SKILL.md` 与 `prompts.md` 有出入时，**以 `prompts.md` 为准**——那里是逐字保留的原始提示词。

## 三条命门

改这个 skill 时最容易破坏的：

1. **第 8 步一次只问一道题，问完停止输出。** 一次列 10 题、或问完自己写答案，等于取消整个环节——测试效应的机制在于用户自己从脑子里往外掏
2. **第 9 步在用户讲清楚之前不进新内容。** 高频失败是写完「请你复述」后自己顺手示范一遍
3. **第 2 步不许跳过。** 它是浅调研和深调研的分水岭

## 已知边界

- **Antigravity 和 WorkBuddy 的加载机制未经一手验证。** 前者按 `AGENTS.md` 约定处理，后者按纯对话粘贴处理。若实际机制不同，在 `build.py` 的 `OUTPUTS` 里加一项即可出新产物
- 方法论与构建管线彼此解耦，调整步骤内容不影响任何适配逻辑
