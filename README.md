# quick-learn-everything

一个**跨 agent 通用**的学习教练 skill。装到 Claude Code、Cursor、ChatGPT、Antigravity、Codex、WorkBuddy 任意一个里，它都会用同一套六步闭环带你吃透一个领域。

> 大多数人只是随意提问，得到随机答案，感觉在学习。一周后什么都不记得。
> 因为真正的学习需要四样东西：**一条路径，一次测试，一次压缩，一个反馈循环。**
> —— Rahul（@sairahul1）

## 方法出处

主线六步出自 **Rahul（@sairahul1）的「6 prompts to learn anything」** —— 把 AI 变成你的老师、考官、资源策展人和学习搭档。**不是为了拿答案，是为了真的学会。**

四要素的落点：**信源 + 阶梯 + 排课 = 路径**，**每课后测验 = 测试**，**费曼循环 = 反馈循环**，**速查表 = 压缩**。

### 顺序不是随便排的

原文对串联顺序有明确要求，两条最容易被搞错：

1. **信源必须最前面** —— 原文写死了「once, **upfront**, **before you start**」。用户想学一个领域，第一时间就该拿到能点开看的东西
2. **测验是每课后跑，不是最后考一次** —— 原文：「**After each study session**, run Quiz Me Until I Break」

### ⚠️ 20 小时，不是 2 小时

原文是「learn [topic] in **20 focused hours**」+「10-session plan, each session lasting **2 hours**」。

坊间的中文转述常把「每节 2 小时」误读成「总共 2 小时」，**差了整整 10 倍** —— 那样每节课只剩 12 分钟，讲不深是必然的。本 skill 按原文的 20 小时执行；时间不够时**减课数，不减每课深度**。

### Co-STORM

两个机制取自斯坦福 OVAL 的 **Co-STORM**（EMNLP 2024，MIT），论文是《Into the Unknown Unknowns: **Engaged Human Learning** through Participation in Language Model Agent Conversations》—— 少数直接研究「人怎么在参与 AI 对话中学习」的工作。

「Unknown unknowns」正是陌生领域最难的地方：你不知道自己缺什么，所以也提不出正确的问题。它的解法是把人放进一场多方对话，全程维护一张**动态 mind map**，论文称之为人与系统之间的「共享概念空间」。**你带走的不是一段对话，而是一棵结构化的概念树。**

| 本 skill | 来自 Co-STORM |
|---|---|
| **第 0 步 热启动** —— 按熟悉度分流，完全陌生的先扫盲 | `warm_start()` |
| **概念树 `mindmap.md`** —— 贯穿六步，自上而下扩展 + 自下而上修剪合并 | `KnowledgeBase.reorganize()` |
| **检索与降级声明** | grounded question generation / answering |

### 检索是编排进流程的，不是「有空就查」

三处不查就是失职：**第 0 步扫盲前**（确认领域的实际词汇，以及这是已确立的术语还是正在形成中的）、**第 1 步信源**（每个资源检索确认存在，拿真链接）、**第 3 步排课**（每节课的资源必须是查到的真材料）。

来源标记分三档，不能混：`[检索:出处]` 读到全文 ｜ `[摘要:出处]` **只看到搜索摘要** ｜ `[未验证]` 模型先验。把摘要说成全文，是在借一个你没有的可信度。无检索能力、或抓取被拦截时，skill 会**按实际情况声明降级**。

## 六步

| 步骤 | 做什么 |
|---|---|
| **0 热启动** | 问主题 / 角色 / **熟悉度**。完全陌生的先扫盲：这东西是什么、核心机制怎么转、10–15 个必知概念 |
| **1 信源前置** | **5 个**最高杠杆资源，每个八项（含难度、适合谁、一条警告）→ 排序 → **七天路径**。**有检索能力就必须给真链接** |
| **2 学习阶梯** | 5 级 × 8 项。**让你永远知道自己在第几级、下一步到哪** |
| **3 核心 20% + 排课** | 找出撬动 80% 的那 20%，排成 **10 节 × 2 小时 = 20 小时** |
| **4 逐课执行** | **真的把课讲了**：讲解 → 给材料 → 动手 → **测验** → 挂树。**每课后都测验**，一次只问一道题 |
| **5 费曼循环** | 讲不清的地方磨平。**讲清楚前不进新内容**，最后给一份可存档的干净解释 |
| **6 一页速查表** | 5 分钟扫完。含**图 / 流程图 / 心智模型**、上场前检查清单、5 个快问快答 |

### 可选 · 深度调研模块

让 5 个互不重叠的视角互相质疑，产出矛盾图谱与自评审。**视角按主题检索后动态生成**（原版 STORM 的做法）；固定的「实践者/学者/怀疑者/经济学家/历史学家」只是兜底——它会在医疗、平台、受监管行业等主题上漏掉最关键的那个视角（当事人、监管者、攻击者）。

**默认不跑。** 它不属于 Rahul 的原方法，是一篇中文转述文章受 STORM 启发添加的。两条硬约束：

- **产出不进考题** —— 它是观点和元分析，观点只能被记住不能被理解，考它必然退化成记忆测验
- **对完全陌生的用户不跑** —— 没有对象级知识打底，五视角只是听不懂的评论

**贯穿全程的概念树**：`mindmap.md` 从第 0 步开始建，每步往上挂新东西。**这是知识本身的载体**，区别于对领域的评论。

**双模式自适应**：能读写文件时产出落到 `./learning/<topic>/`，跨会话续学；纯对话环境全部在对话内给出。

**对话里始终承载实质内容** —— 文件是持久化副本，不是交付通道，**用户从不打开任何文件也应该完整拿到学习内容**。建目录时 skill 会主动说清文件在哪、远程容器里看不到且会被回收、怎么带走 —— 因为用户不知道自己需要下指令才能拿到文件，**说明的责任在 agent**。

> 📁 `learning/` 已写进 `.gitignore`。想跨机器保留进度，删掉那一行或 `git add -f learning/<topic>`。

## 安装

### Claude Code / Claude 系

**在本仓库里直接用** —— clone 下来打开就行，`.claude/skills/` 已经配好（符号链接指向根目录的源文件，不会有副本漂移）：

```bash
git clone https://github.com/vivilin-ai/quick-learn-everything.git
cd quick-learn-everything    # 说「我想快速入门 XX」即可触发
```

**装到全局，任何项目都能用**：

```bash
mkdir -p ~/.claude/skills/quick-learn-everything
cp -r SKILL.md references ~/.claude/skills/quick-learn-everything/
```

**装到你自己的某个项目**：把 `SKILL.md` 和 `references/` 拷进 `<你的项目>/.claude/skills/quick-learn-everything/`。

### Cursor

把 `.cursor/rules/quick-learn-everything.mdc` 拷进项目的 `.cursor/rules/`。该文件自包含（参考资料已内联），单独拷贝即可。

规则设的是 `alwaysApply: false`，靠 description 按需触发，不污染日常对话。

### Codex / Antigravity / 其他遵循 AGENTS.md 约定的 agent

把 `AGENTS.md` 放到项目根目录，已有的话追加进去。同样自包含。

### ChatGPT / WorkBuddy / 其他纯对话环境

这类环境读不到仓库文件，用 `dist/` 下的单文件版本：

- **`dist/PROMPT.md`** —— 完整版（约 32k 字符），含六个原始提示词、方法论展开和全部产出模板。粘贴到对话开头
- **`dist/PROMPT-compact.md`** —— 精简版（约 5.0k 字符）。用于 Custom GPT 的 Instructions，那里有 **8000 字符硬上限**。保留六步骨架、命门规则和防幻觉规则，裁掉产出模板

### 只想手动跑，不装 skill

`references/prompts.md` 里是**六个原始提示词全文（英文原文逐字保留）**，替换 `【】` 里的内容，一步一步贴给任何 AI 即可。

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
SKILL.md                    ★ 源：Agent Skills 格式，六步骨架
references/                 ★ 源：按需加载
  prompts.md                  六个原始提示词全文（权威规格）
  method.md                   每步的展开、判据、常见失败模式、方法出处
  deep-research.md            可选模块（五视角）的完整说明
  source-quality.md           第 1 步的信源筛选标准 + 防幻觉规则
  templates/                  落盘模式的产出骨架
    mindmap.md                  概念树，贯穿全程
    resources.md                第 1 步
    learning-plan.md            第 2–3 步
    drill-log.md                第 4–5 步
    cheatsheet.md               第 6 步
    research-brief.md           可选模块
    progress.md                 跨会话进度
scripts/build.py            构建 + 校验
AGENTS.md                   ⚙ 产物
.cursor/rules/*.mdc         ⚙ 产物
dist/PROMPT*.md             ⚙ 产物
```

`SKILL.md` 与 `prompts.md` 有出入时，**以 `prompts.md` 为准**——那里是逐字保留的原始提示词。

## 四条命门

改这个 skill 时最容易破坏的：

1. **第 4 步不许跳过。** 排完课不等于学完课 —— 早期版本就是漏了它，排完 10 节课的计划直接开考，用户被考的是**从未交付过的内容**
2. **测验一次只问一道题，问完停止输出。** 一次列 10 题、或问完自己写答案，等于取消整个环节 —— 测试效应的机制在于用户自己从脑子里往外掏
3. **第 5 步在用户讲清楚之前不进新内容。** 高频失败是写完「请你复述」后自己顺手示范一遍
4. **20 小时不是 2 小时。** 时间不够减课数，不减每课深度

## 已知边界

- **Antigravity 和 WorkBuddy 的加载机制未经一手验证。** 前者按 `AGENTS.md` 约定处理，后者按纯对话粘贴处理。若实际机制不同，在 `build.py` 的 `OUTPUTS` 里加一项即可出新产物
- 方法论与构建管线彼此解耦，调整步骤内容不影响任何适配逻辑
