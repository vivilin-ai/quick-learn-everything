# quick-learn-everything

一个**跨 agent 通用**的学习教练 skill。装到 Claude Code、Cursor、ChatGPT、Antigravity、Codex、WorkBuddy 任意一个里，它都会用同一套方法带你从「一无所知」到「能独立判断、能与内行对话」。

核心取向：**你是教练，不是百科全书。** 成败取决于用户最后能输出什么，而不是 agent 讲了多少。

## 它做什么

被唤起后走七个阶段，一次只推进一个，每个阶段停下来等你反馈：

| 阶段 | 做什么 |
|---|---|
| **Phase 0** 澄清目标 | 问清目的场景、现有基础、时间预算、验收标准。同样是学 K8s，为面试和为救火是两条路 |
| **Phase 1** 领域地图 | 5–9 个模块的全景，标出核心 20%、可忽略的枝节、以及领域内的争议点 |
| **Phase 2** 术语表 | 黑话解码。含别名对照和「假朋友」——那些看着像日常词其实不是的 |
| **Phase 3** 精选信源 | 分级推荐，**并说出不推荐什么及原因** |
| **Phase 4** 学习路径 | 带时间刻度的里程碑。排序遵循「先能用，再懂原理」 |
| **Phase 5** 主动学习循环 | 讲解 → 复述 → 诊断 → 测验，逐个里程碑循环。**真正产生学习的环节** |
| **Phase 6** 实践与结业 | 小项目 + 对照验收标准诚实复盘 |

**双模式自适应**：能读写文件时，产出落到 `./learning/<topic>/`，跨会话续学（每次先读 `progress.md` 恢复进度）；纯对话环境则全部在对话内给出。

## 安装

### Claude Code / Claude 系

```bash
git clone https://github.com/vivilin-ai/quick-learn-everything.git
mkdir -p ~/.claude/skills/quick-learn-everything
cp -r quick-learn-everything/{SKILL.md,references} ~/.claude/skills/quick-learn-everything/
```

只想在某个项目里用，就放 `<项目>/.claude/skills/` 下。之后说「我想快速入门 XX」会自动触发。

### Cursor

把 `.cursor/rules/quick-learn-everything.mdc` 拷进你项目的 `.cursor/rules/`。该文件是自包含的（参考资料已内联），单独拷贝即可，不需要带 `references/`。

规则设的是 `alwaysApply: false`，靠 description 按需触发，不会污染日常对话。

### Codex / Antigravity / 其他遵循 AGENTS.md 约定的 agent

把 `AGENTS.md` 放到项目根目录。已有 `AGENTS.md` 的话，把内容追加进去。同样是自包含的。

### ChatGPT / WorkBuddy / 其他纯对话环境

这类环境读不到仓库文件，用 `dist/` 下的单文件版本：

- **`dist/PROMPT.md`** —— 完整版。粘贴到对话开头，然后说出你想学的领域
- **`dist/PROMPT-compact.md`** —— 精简版（约 3.6k 字符）。用于 Custom GPT 的指令框，那里有 **8000 字符硬上限**。保留了七个阶段、硬性规则和防幻觉规则，裁掉了产出模板

放进 ChatGPT 的 Projects 指令、Custom GPT 的 Instructions，或直接贴进对话都行。

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

**不要手改产物文件**——下次构建会覆盖掉。`--check` 就是为了在 CI 里拦住这种漂移。

构建时会强制三件事：

1. `PROMPT-compact.md` 正文 ≤ 8000 字符，超了直接报错而不是静默截断
2. 自包含产物里不留任何 `references/xxx.md` 这类悬空引用（粘贴进 ChatGPT 后会指向虚空）
3. 产物里不残留 `compact:skip` / `compact:include` 构建标记

### 两个构建标记

写在源文件里，控制内容进哪个产物：

```markdown
<!-- compact:skip -->    包裹的段落不进精简版（写在 SKILL.md 里）
<!-- compact:include --> 包裹的段落要进精简版（写在 references/ 里）
```

两种标记在所有产物中都会被剥掉，只影响内容取舍。

## 仓库结构

```
SKILL.md                    ★ 源：Agent Skills 格式，正文精简
references/                 ★ 源：按需加载的细节
  method.md                   各阶段展开：判据、常见失败模式
  prompts.md                  各阶段可直接用的话术模板
  source-quality.md           信源筛选标准 + 防幻觉规则
  templates/                  落盘模式的产出文件骨架
scripts/build.py            构建 + 校验
AGENTS.md                   ⚙ 产物
.cursor/rules/*.mdc         ⚙ 产物
dist/PROMPT*.md             ⚙ 产物
```

## 已知边界

- **Antigravity 和 WorkBuddy 的加载机制未经一手验证。** 前者按 `AGENTS.md` 约定处理，后者按纯对话粘贴处理。如果实际机制不同，加一个适配产物的成本很低——在 `build.py` 的 `OUTPUTS` 里加一项即可
- 方法论目前基于通用的快速入门实践。骨架与构建管线彼此独立，替换 Phase 内容不影响任何适配逻辑
