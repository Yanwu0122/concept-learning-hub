# 学习笔记体系 · 个人知识库

本目录是 `concept-learning-hub` 的个人知识库：**一个概念 = 一份笔记**，每份笔记由项目级 Skill（`.workbuddy/skills/concept-learning-generator/`）按统一结构生成。库内维护「机器可读登记册 + 自动分类 + 交互门户」，方便持续沉淀、检索与复习。

## 🧭 知识库门户

- **`hub.html`** —— 知识库入口页：按领域分区展示所有笔记卡片，支持**关键词实时搜索**（概念名/标签/摘要）与**随机复习**（🎲 抽一份笔记打开）。本地双击即可使用。
- **`catalog.json`** —— 机器可读登记册（数据真源）：记录每份笔记的**领域、标签、摘要**。新增内容只改它，门户由脚本自动重建。

## 领域分类体系

素材入库时由 `knowledge-organizer` Skill 自动识别领域（读内容判定，不是看文件名）：

| domain | 领域 | 现有笔记 |
|--------|------|---------|
| `overview` | 🗺️ 知识地图（关系总览） | concept-relationship |
| `llm` | 🧠 大模型与生成式 AI | llm、llm-context |
| `agent` | 🤖 智能体与自动化 | agent、skill |
| `ml-basics` | 🧬 机器学习基础（可扩展） | — |
| `engineering` | 🛠️ AI 工程与工具（可扩展） | — |
| `general` | 📚 通用与未分类 | — |

## 目录约定

- 概念笔记统一存放于本目录（`learning-materials/`），**不放其他位置**
- 命名：`<概念英文名小写>.html`，多词用连字符连接（如 `llm-context.html`）
- 概念之间的关系说明：根目录的 `concept-relationship.md`（含 Mermaid 图）+ 网页版 `concept-relationship.html`
- 生成素材与中间 JSON：临时文件放仓库根 `.tmp/`（已被 `.gitignore` 排除，不会提交）
- 每份笔记必须包含：学习目标、核心问题、概念解释（个人解释＋核心机制＋关键特征）、应用场景、概念辨析、自测问题、参考来源

## 笔记清单（按领域）

| 笔记文件 | 概念 | 领域 | 一句话主题 |
|---------|------|------|-----------|
| `concept-relationship.html` | 概念关系总览 | 🗺️ 知识地图 | 上下文影响 Agent、Skill 沉淀知识 |
| `llm.html` | LLM（大语言模型） | 🧠 大模型与生成式 AI | 训练三阶段 / Transformer / 能力边界 / llm-wiki-agent 案例 |
| `llm-context.html` | 大模型的上下文 | 🧠 大模型与生成式 AI | 上下文窗口 / Token / 注意力 |
| `agent.html` | Agent | 🤖 智能体与自动化 | 感知-推理-行动与工具调用 |
| `skill.html` | Skill | 🤖 智能体与自动化 | 可复用能力包的结构与执行 |
| `concept-relationship.md`（根目录） | 三者关系 | 🗺️ 知识地图 | 关系说明的 Markdown 版 |

## 如何把新素材「自动分类」收进知识库

1. 把原始素材（网页链接、文章、课件摘录、随手记）放进仓库根目录的 `inbox/`，或直接粘贴给 AI
2. 对助手说：「**把 inbox 里的内容整理进知识库**」（或「帮我学习并归档 XX」）
3. `knowledge-organizer` Skill 自动执行：**读内容 → 识别领域 → 查重**（同主题并入已有笔记，否则新建）→ 生成/整理笔记 → **登记 catalog.json** → 重建 hub.html → 更新本清单 → 推送
4. 概念型内容会走 `concept-learning-generator` 的标准流水线（调研 → 结构化 → 渲染 HTML），保证七大结构齐全

> 想只生成单份概念笔记（不涉及归档）时，直接说「用概念学习资料生成 Skill 学习一下 XXX」即可，产出后别忘了登记到 catalog（或让 organizer 顺手收尾）。

## 学习顺序建议

`Agent` → `大模型的上下文` → `Skill` → `LLM`。`LLM` 是「能力层」，上下文是「使用层」，Skill 是把能力与流程沉淀成可复用资产，Agent 则是把三者串起来干活的主体。
