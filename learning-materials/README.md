# 学习笔记体系

本目录是 `concept-learning-hub` 的概念学习笔记库：**一个概念 = 一份笔记**，每份笔记由项目级 Skill（`.workbuddy/skills/concept-learning-generator/`）按统一结构生成，便于横向对比、追溯来源与持续扩充。

## 目录约定

- 笔记文件统一存放于本目录（`learning-materials/`），**不放其他位置**
- 命名：`<概念英文名小写>.html`，多词用连字符连接（如 `llm-context.html`、`concept-relationship.html`）
- 概念之间的关系说明：根目录的 `concept-relationship.md`（Markdown，便于阅读与图表渲染）
- 生成素材与中间 JSON：临时文件放仓库根 `.tmp/`（已被 `.gitignore` 排除，不会提交）
- 每份笔记必须包含：学习目标、核心问题、概念解释（个人解释＋核心机制＋关键特征）、应用场景、概念辨析、自测问题、参考来源

## 笔记清单

| 笔记文件 | 概念 | 一句话主题 | 状态 |
|---------|------|-----------|------|
| `agent.html` | Agent | 感知-推理-行动与工具调用 | ✅ |
| `llm-context.html` | 大模型的上下文 | 上下文窗口 / Token / 注意力 | ✅ |
| `skill.html` | Skill | 可复用能力包的结构与执行 | ✅ |
| `llm.html` | LLM（大语言模型） | 训练三阶段 / Transformer / 能力边界 / llm-wiki-agent 案例 | ✅ |
| `concept-relationship.html` | 三者关系 | 上下文影响 Agent、Skill 沉淀知识 | ✅ |
| `concept-relationship.md`（根目录） | 三者关系 | 关系说明的 Markdown 版（含 Mermaid 图） | ✅ |

## 如何新增一份概念笔记

1. 在 WorkBuddy 中打开本仓库，对助手说：「用概念学习资料生成 Skill 学习一下 XXX」
2. Skill 会按流程执行：调研（web 检索权威来源）→ 结构化组织内容 → 构建 JSON → 调用脚本渲染 HTML：
   ```bash
   python .workbuddy/skills/concept-learning-generator/scripts/generate_learning_material.py \
     --input '<内容JSON>' --output learning-materials/<概念名>.html
   ```
3. 产出后按 SKILL.md 的「自检要求」逐项核查：结构齐全、来源真实可访问、无整段照搬、HTML 可独立打开
4. 把新笔记登记到上表，并更新仓库根目录 `README.md` 的目录树与资料表格
5. 提交并 push 到 GitHub

> 学习顺序建议：`Agent` → `大模型的上下文` → `Skill` → `LLM`。`LLM` 是「能力层」，上下文是「使用层」，Skill 是把能力与流程沉淀成可复用资产，Agent 则是把三者串起来干活的主体。
