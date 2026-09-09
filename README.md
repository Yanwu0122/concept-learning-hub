# Concept Learning Hub

一个用于沉淀概念学习资料的个人学习仓库。内含一个可复用的「概念学习资料生成 Skill」，以及由该 Skill 生成并经本人核查的学习资料。

## 仓库用途

本仓库从课堂作业起步，定位是**可持续迭代的个人知识库**，用于：
- 保存项目级 Skill：概念学习生成器 `concept-learning-generator`（调研 → 内容组织 → HTML 渲染）+ 知识库管家 `knowledge-organizer`（自动识别领域、分门别类、登记入库）
- 保存由 Skill 生成并经本人核查的概念学习资料（Agent、大模型的上下文、Skill、LLM 等）
- 说明概念之间的关系
- 提供分类登记（catalog.json）、搜索与复习门户（hub.html）和素材投递口（inbox/）
- 作为后续课程项目继续沉淀学习资料的个人工具基础与作品集材料

## 目录结构

```text
concept-learning-hub/
├── .workbuddy/
│   └── skills/
│       ├── concept-learning-generator/          # Skill 1：概念学习资料生成
│       │   ├── SKILL.md                            # Skill 核心文件
│       │   ├── references/
│       │   │   └── color-schemes.md                # 配色方案参考
│       │   └── scripts/
│       │       └── generate_learning_material.py  # HTML 渲染脚本
│       └── knowledge-organizer/                 # Skill 2：知识库管家（自动分类入库）
│           ├── SKILL.md                            # Skill 核心文件
│           └── scripts/
│               └── rebuild_hub.py                 # 读 catalog.json 重建门户 hub.html
├── learning-materials/                         # 知识库主体
│   ├── README.md                                # 笔记体系索引、领域分类、入库规范
│   ├── hub.html                                 # 🧭 知识库门户（搜索 + 领域分区 + 复习）
│   ├── catalog.json                             # 登记册：每份笔记的领域/标签/摘要
│   ├── agent.html                               # Agent 概念学习资料
│   ├── llm-context.html                         # 大模型的上下文
│   ├── skill.html                               # Skill 概念学习资料
│   ├── llm.html                                 # LLM（大语言模型）概念学习资料
│   └── concept-relationship.html                # 三者关系（网页版）
├── inbox/                                       # 📥 素材投递口（放原始资料待归类）
│   └── README.md
├── concept-relationship.md                      # 三者关系说明（Markdown 版）
├── README.md
└── .gitignore
```

## Skill 存放路径

项目级 Skill 位于 `.workbuddy/skills/concept-learning-generator/`，核心文件为 `SKILL.md`，其顶部包含 YAML 元数据（`name`、`description`），并明确描述了适用场景、输入信息、生成步骤、输出结构、资料来源要求与自检要求。

## 如何在 WorkBuddy 中调用该 Skill

1. 在 WorkBuddy 中打开本仓库，将其作为当前项目。
2. 直接对助手说类似「帮我学习一下 XXX 这个概念」或「用概念学习资料生成 Skill 整理 XXX 的学习笔记」。
3. 助手会识别到匹配场景，自动加载 `.workbuddy/skills/concept-learning-generator/` 下的 Skill，按既定流程生成结构化学习资料。
4. 生成的成果是一份独立的 HTML 学习资料，包含学习目标、核心问题、概念解释、应用场景、概念辨析、自测检验与参考来源。

Skill 是可复用的：给它任意一个新概念名，它都能按统一结构产出学习资料，不限于本仓库已有的概念。

**知识库管家（knowledge-organizer）**：对 AI 说「把 XX 收进知识库 / 整理 inbox / 学一个新概念并归档」，它会自动识别素材领域 → 分门别类（同主题并入已有笔记，新主题走生成器）→ 登记 catalog → 重建门户 → 推送。详细流程见其 `SKILL.md`。

## 学习笔记体系（知识库）

本仓库以 `learning-materials/` 作为知识库主体，**索引、领域分类与入库规范见 [learning-materials/README.md](learning-materials/README.md)**。

- 🧭 **知识库门户**：打开 [learning-materials/hub.html](learning-materials/hub.html)（本地双击即可）——按领域分区浏览全部笔记，支持关键词实时搜索与「随机复习」。
- 🗂️ **自动分类登记**：每份笔记在 [catalog.json](learning-materials/catalog.json) 中登记领域与标签；`knowledge-organizer` Skill 会把新素材自动识别领域、分门别类地收进来。
- 📥 **素材投递口**：把想学的网页/文章/课件丢进 [inbox/](inbox/)，对 AI 说「把 inbox 里的内容整理进知识库」即可。

## 已生成的学习资料

| 文件 | 对应概念 | 说明 |
|------|---------|------|
| `agent.html` | Agent（智能代理） | 定义、感知-推理-行动机制、应用与边界 |
| `llm-context.html` | 大模型的上下文 | 上下文窗口、Token、注意力机制与影响 |
| `skill.html` | Skill（技能包） | 定义、组成结构、执行模式与复用价值 |
| `llm.html` | LLM（大语言模型） | 训练三阶段、Transformer、能力边界与 llm-wiki-agent 案例 |
| `concept-relationship.html` | 三者关系 | 上下文如何影响 Agent，Skill 如何沉淀知识 |
| `README.md` | 笔记索引 | 体系说明：目录约定、文件清单、如何新增笔记 |

资料均使用本仓库的 Skill 生成，并经过本人阅读、理解与核查，资料中的来源链接均真实可访问。

## 使用 AI 后的人工核查

在使用 AI 协助组织本仓库过程中，我做了以下人工核查与修改：
- 逐个阅读并核对了各份学习资料的核心表述，确保概念解释准确、无证据性错误。
- 核查所有参考来源链接均可访问，并补充了官方与权威来源；移除了不可验证的占位链接。
- 复核了 concept-relationship 中对「上下文—Agent—Skill」关系的描述，确保符合课程理解。
- 检查了 Skill 的目录结构与 YAML 元数据符合规范。

## 版本与安全

本仓库已通过 Git 进行版本管理并推送至 GitHub。`.gitignore` 已配置，确保不提交 API Key、密码、个人隐私等敏感信息。
