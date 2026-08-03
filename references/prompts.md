# 原始提示词

**权威规格。** `SKILL.md` 里每一步的产出要求都源自这里；两处有出入时以本文件为准。

作为 agent 执行时按这些要求产出，但**不要把提示词原文念给用户听**。用户想自己手动驱动时，把对应那段拷走，替换 `[topic]` 即可。

---

# Rahul（@sairahul1）的六个提示词

> 逐字保留英文原文。原帖的定位：**「Not for getting answers. For actually learning.」**
>
> 原文对四要素的表述：
> → **A path** — so you know what to learn in what order
> → **A test** — so you find out what you don't actually know
> → **A compression** — so you can review fast before you need it
> → **A feedback loop** — so gaps get caught and fixed immediately

## 原文的串联顺序

> → Start with the **Learning Ladder** to see the whole map
> → Use **20 Hours** to find the core 20% worth focusing on first
> → **After each study session**, run **Quiz Me Until I Break** to find real gaps
> → Compress what you've learned into a **One-Page Cheat Sheet** for fast review
> → Use **Signal in the Noise once, upfront, to pick your 5 resources before you start**
> → Run the **Feynman Loop** on anything that still feels shaky
>
> **Path → test → compress → repeat.**

⚠️ 两处最容易被搞错：**信源要 upfront**（所以本 skill 把它排成第 1 步），**测验是每课后跑**（不是最后考一次大的）。

---

## ① Learning Ladder → 本 skill 第 2 步

```
I want to learn [topic] step by step, without skipping important foundations.

Act like an expert teacher and skill coach. Break [topic] into 5 clear difficulty levels, from complete beginner to confident practitioner.

For each level, include:

1. Level name
2. What I should understand at this stage
3. What mastery looks like at this level
4. The most important concepts or skills to focus on
5. One milestone that proves I am ready to move forward
6. One hands-on exercise or mini-project
7. Common mistakes learners make at this level
8. A simple self-check question before moving to the next level

Structure the levels like this:
- Level 1: Complete Beginner
- Level 2: Basic Understanding
- Level 3: Practical User
- Level 4: Problem Solver
- Level 5: Confident Practitioner

Keep the explanation practical, beginner-friendly, and focused on real progress.
```

> 作用：**你永远知道自己站在哪一级、下一步该到哪。** 大多数人学不下去，是因为基础没牢就去啃高级材料。

## ② Learn Anything in 20 Hours → 本 skill 第 3 步

```
I want to learn [topic] in 20 focused hours.

Act like an expert teacher and learning strategist. Your job is to help me learn the most useful parts first, not everything.

Please do the following:

1. Identify the 20% of concepts, skills, or principles that will give me 80% of the real-world results.
2. Explain why these core areas matter and how they connect to practical use.
3. Create a 10-session learning plan, with each session lasting 2 hours.
4. For every session, include:
   - Main learning goal
   - Key concepts to study
   - One practical exercise or mini-project
   - One recommended resource, preferably free or beginner-friendly
   - Expected outcome after completing the session
5. At the end of each session, give me 5 review questions to test my understanding.
6. After the full plan, suggest one final project that proves I understand the topic well enough to use it in real life.

Keep the plan beginner-friendly, practical, and focused on fast progress.
```

> 🚨 **20 focused hours**，**10 sessions × 2 hours each**。不是总共 2 小时——那个误读会让每节课只剩 12 分钟，深度必然不够。时间不足时**减课数，不减每课深度**。

## ③ Quiz Me Until I Break → 本 skill 第 4 步的测验环节（每课后跑）

```
I just studied [topic], and I want to test how well I really understand it.

Act like a strict but helpful examiner. Your job is to find the edge of my understanding through active recall.

Start by asking me 10 questions, one at a time.

Rules:

1. Make the questions progressively harder:
   - Questions 1-3: beginner level
   - Questions 4-6: intermediate level
   - Questions 7-8: advanced level
   - Questions 9-10: expert level

2. Ask only one question at a time and wait for my answer.

3. After each answer, do four things:
   - Grade my answer out of 10
   - Tell me what I got right
   - Identify the exact gap, mistake, or weak point
   - Re-explain only the part I missed in simple language

4. If my answer is weak, ask one follow-up question before moving on.

5. If I answer well, increase the difficulty slightly.

6. At the end, give me:
   - My final score
   - My strongest areas
   - My weakest areas
   - A short revision plan
   - 5 final challenge questions to master the topic

Do not give me all answers at once. Make this feel like a real learning interview.
```

> 🚨 **最容易被违反、危害最大的一条：一次列出所有题、或问完自己把答案写上。** 那等于取消整个环节——测试效应的机制在于用户自己从脑子里往外掏。**问完一题就停止输出。**

## ④ One-Page Cheat Sheet → 本 skill 第 6 步

```
I want a one-page cheat sheet for [topic].

Act like an expert teacher who can simplify complex ideas into a fast review sheet.

Create a cheat sheet that I can review in 5 minutes before I need to use the topic.

Please include:

1. A short definition of the topic in simple language.
2. The most important concepts, rules, formulas, or steps.
3. Clear bullet points instead of long paragraphs.
4. A simple labeled diagram, flowchart, table, or mental model if it helps explain the topic.
5. 3-5 concrete examples that show how the topic works in real life.
6. Common mistakes or confusing parts I should avoid.
7. A quick "Before You Use This" checklist.
8. 5 rapid-fire questions to test my memory.

Keep it practical, visual, beginner-friendly, and easy to scan.
```

> 第 4 项（图 / 流程图 / 表格 / 心智模型）容易被漏掉，而它正是「记结构比记段落牢」的落点。

## ⑤ Signal in the Noise → 本 skill **第 1 步**（前置）

```
I want to learn [topic] fast, but I do not want to waste time on low-quality resources.

Act like an expert learning curator. Find the 5 highest-leverage resources for learning [topic].

The resources can include books, videos, courses, websites, newsletters, communities, or experts to follow.

For each resource, include:

1. Resource name
2. Type of resource
3. Why it is worth my time
4. What specific part of [topic] it helps me learn
5. Best learner type for this resource
6. Difficulty level: beginner, intermediate, or advanced
7. How I should use it effectively
8. One warning about what not to waste time on

After the list, rank the resources in the best order to use them.

Then give me a simple 7-day learning path using only these resources.

Focus on quality, clarity, and practical usefulness. I want the signal, not the noise.
```

> 原文明确要求 **once, upfront, before you start** —— 所以它在本 skill 里是**第 1 步**，不是排在分析之后。
> 有检索能力时**必须检索出真链接**，不要凭记忆报书名。

## ⑥ Feynman Loop → 本 skill 第 5 步

```
I want to understand [topic] deeply using the Feynman learning method.

Act like a patient teacher. First, explain [topic] to me in simple language, as if I am 12 years old.

Use:
- simple words
- real-life examples
- analogies
- no unnecessary jargon
- short explanations

After explaining, ask me to explain the topic back in my own words.

Then review my explanation and do the following:

1. Identify what I explained correctly.
2. Find every gap, mistake, confusion, or missing idea.
3. Re-teach only the parts I got wrong or missed.
4. Ask me to explain it again in a cleaner way.
5. Repeat this loop until my explanation is simple, accurate, and complete.

Rules:
- Do not move forward until my explanation is clear.
- Do not overload me with extra theory.
- Correct me gently but clearly.
- Use examples whenever I am confused.
- At the end, give me a final clean explanation of [topic] that I can save as notes.

Make this feel like an interactive learning conversation, not a lecture.
```

> 🚨 **第二个高频失败：写完「请你复述一遍」之后，自己顺手示范了一遍。** 写完提问就停止输出。
> 最后一条（给一份可存档的干净解释）容易被漏掉。

---

# 可选模块 · 深度调研的中文提示词

> ⚠️ **不属于 Rahul 的原方法。** 这四段出自一篇中文转述文章，作者受斯坦福 STORM 启发自行添加。
> 默认不跑，且**产出不进考题**。理由见 `references/deep-research.md`。

## 环节一 · 五视角

```
我要研究【你的主题】。
请模拟 5 位不同的专家，从各自的视角分析这个主题：

1. 实践者：每天跟这东西打交道的人。
   他们知道哪些学者不知道的事？哪些实际情况总是被忽略？
2. 学者：研究这个领域多年的人。
   同行评审的证据到底说了什么？证据在哪些地方和大众认知相反？
3. 怀疑者：认为主流观点有问题的人。
   最强的反方论点是什么？支持者们刻意忽略了哪些证据？
4. 经济学家：盯着钱流向的人。
   谁在从当前的叙事里获利？哪些利益在影响这个领域的结论？
5. 历史学家：见过类似规律的人。
   历史上有什么相似的先例？那些先例最后是怎么收场的？

每个视角请给我：
- 两句话说清他的核心立场
- 支持他观点的最强证据
- 一件只有他会告诉我、其他视角绝不会提的事
```

## 环节二 · 矛盾图谱

```
基于上面 5 个视角，给我画一张矛盾图：
哪些视角在直接冲突，各自的依据是什么；
谁的证据最强、谁的最弱、为什么；
哪一个问题一旦有答案，就能化解最大的矛盾；
所有视角都同意的是什么（这大概率是真的）；
没有任何视角提到的是什么（这可能是整个领域的盲区）。
```

## 环节三 · 综合简报

```
把 5 个视角和矛盾图综合成一份调研简报：
一段话总结（讲给只有 60 秒的 CEO 听，要细节，不要标题党）；
5 个关键发现，按可靠性排序，标注哪些视角支持、哪些反对；
一个只有把 5 个视角放在一起才能看到的隐藏关联；
一条具体的行动建议（以我的角色，我该做什么不一样的事）；
一个前沿问题（它的答案会改变我们对这个主题的全部理解）。
```

## 环节四 · 同行评审自检

```
现在请你对刚才这份简报做一次同行评审：
给 5 个关键发现逐个打 1-10 的可靠性分，并解释理由；
你最没把握的是哪个结论，需要什么信息才能验证它；
哪个视角在综合时占的比重过大了；
有没有第 6 个视角是该加进来、加了会改变结论的；
如果一位斯坦福教授来评审这份简报，会打几分，会让我改什么。
```
