#!/usr/bin/env python3
"""概念学习资料HTML生成器: 将结构化JSON内容渲染为学习友好型HTML页面"""

import argparse
import json
import sys


COLOR_SCHEMES = {
    "deep_ocean": {
        "name": "深海蓝",
        "bg": "#F7F9FA", "card_bg": "#FFFFFF", "primary": "#2C3E50",
        "secondary": "#34495E", "accent": "#5D7B93", "highlight": "#7F8C8D",
        "text_main": "#1A252F", "text_secondary": "#4A5568", "border": "#D5DDE3",
        "tag_bg": "#E8EDF1", "tag_color": "#2C3E50", "quote_bg": "#EDF1F4",
        "quote_border": "#5D7B93", "objective_bg": "#EDF2F7",
        "objective_icon": "#2C3E50", "test_bg": "#F0F4F8",
        "test_border": "#5D7B93", "source_link": "#34495E",
    },
    "twilight_purple": {
        "name": "暮光紫",
        "bg": "#F8F6FA", "card_bg": "#FFFFFF", "primary": "#4A3B5C",
        "secondary": "#5D4E6D", "accent": "#7B6B8A", "highlight": "#8E7C9E",
        "text_main": "#2D1F3D", "text_secondary": "#5A4A6B", "border": "#D8D0E0",
        "tag_bg": "#EDE8F2", "tag_color": "#4A3B5C", "quote_bg": "#F0ECF4",
        "quote_border": "#7B6B8A", "objective_bg": "#F3EFF8",
        "objective_icon": "#4A3B5C", "test_bg": "#F5F0FA",
        "test_border": "#7B6B8A", "source_link": "#5D4E6D",
    },
    "forest_green": {
        "name": "森林绿",
        "bg": "#F5F8F6", "card_bg": "#FFFFFF", "primary": "#2D4A3E",
        "secondary": "#3D5C4E", "accent": "#5A7B6A", "highlight": "#6E8F7E",
        "text_main": "#1A2F26", "text_secondary": "#3D5C4E", "border": "#C8D8D0",
        "tag_bg": "#E2EDE8", "tag_color": "#2D4A3E", "quote_bg": "#E8F0EC",
        "quote_border": "#5A7B6A", "objective_bg": "#ECF5F0",
        "objective_icon": "#2D4A3E", "test_bg": "#F0F7F3",
        "test_border": "#5A7B6A", "source_link": "#3D5C4E",
    },
    "warm_grey": {
        "name": "暖灰棕",
        "bg": "#F8F6F4", "card_bg": "#FFFFFF", "primary": "#4A4039",
        "secondary": "#5C524A", "accent": "#7B6E63", "highlight": "#8E8074",
        "text_main": "#2D2520", "text_secondary": "#5C524A", "border": "#D8D0C8",
        "tag_bg": "#EDE8E3", "tag_color": "#4A4039", "quote_bg": "#F0ECE8",
        "quote_border": "#7B6E63", "objective_bg": "#F5F0EB",
        "objective_icon": "#4A4039", "test_bg": "#F8F3EE",
        "test_border": "#7B6E63", "source_link": "#5C524A",
    }
}

FONT_FAMILY = "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', sans-serif"


def escape_html(text):
    """转义HTML特殊字符"""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


def generate_css(scheme):
    """生成CSS样式"""
    return f"""    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {FONT_FAMILY}; background: {scheme['bg']}; color: {scheme['text_main']}; line-height: 1.8; padding: 40px 20px; }}
    .container {{ max-width: 820px; margin: 0 auto; }}
    .header {{ margin-bottom: 36px; padding-bottom: 24px; border-bottom: 2px solid {scheme['primary']}; }}
    .header-concept {{ font-size: 32px; font-weight: 700; color: {scheme['primary']}; margin-bottom: 4px; }}
    .header-concept-zh {{ font-size: 20px; font-weight: 400; color: {scheme['secondary']}; margin-left: 12px; }}
    .header-subtitle {{ font-size: 15px; color: {scheme['highlight']}; margin-top: 8px; }}
    .section {{ margin-bottom: 28px; background: {scheme['card_bg']}; border-radius: 8px; padding: 24px 28px; border: 1px solid {scheme['border']}; }}
    .section-title {{ font-size: 18px; font-weight: 700; color: {scheme['primary']}; margin-bottom: 16px; padding-left: 12px; border-left: 4px solid {scheme['primary']}; }}
    .objectives {{ background: {scheme['objective_bg']}; border-radius: 8px; padding: 20px 24px; margin-bottom: 28px; }}
    .objectives-title {{ font-size: 16px; font-weight: 700; color: {scheme['objective_icon']}; margin-bottom: 12px; }}
    .objectives li {{ font-size: 15px; color: {scheme['text_main']}; margin-bottom: 6px; margin-left: 20px; line-height: 1.8; }}
    .core-questions {{ margin-bottom: 28px; }}
    .core-question {{ font-size: 15px; color: {scheme['secondary']}; padding: 8px 16px; margin-bottom: 6px; background: {scheme['tag_bg']}; border-radius: 6px; }}
    .core-question::before {{ content: 'Q: '; font-weight: 700; color: {scheme['primary']}; }}
    .interpretation {{ font-size: 15px; color: {scheme['text_main']}; line-height: 2; margin-bottom: 20px; padding: 16px 20px; background: {scheme['quote_bg']}; border-radius: 0 8px 8px 0; border-left: 3px solid {scheme['quote_border']}; }}
    .mechanism-list {{ margin-bottom: 20px; }}
    .mechanism-item {{ margin-bottom: 14px; padding-left: 16px; border-left: 2px solid {scheme['accent']}; }}
    .mechanism-title {{ font-size: 15px; font-weight: 600; color: {scheme['secondary']}; margin-bottom: 4px; }}
    .mechanism-desc {{ font-size: 14px; color: {scheme['text_main']}; line-height: 1.8; }}
    .features {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
    .feature-tag {{ font-size: 13px; color: {scheme['tag_color']}; background: {scheme['tag_bg']}; padding: 6px 14px; border-radius: 20px; font-weight: 500; }}
    .scenario {{ margin-bottom: 20px; }}
    .scenario-title {{ font-size: 16px; font-weight: 600; color: {scheme['secondary']}; margin-bottom: 10px; }}
    .scenario-context {{ font-size: 15px; color: {scheme['text_main']}; line-height: 1.9; margin-bottom: 12px; }}
    .scenario-analysis {{ font-size: 14px; color: {scheme['text_secondary']}; line-height: 1.9; padding: 14px 18px; background: {scheme['quote_bg']}; border-radius: 6px; }}
    .scenario-analysis::before {{ content: '概念映射: '; font-weight: 600; color: {scheme['accent']}; }}
    .confusion-item {{ margin-bottom: 16px; padding: 14px 18px; background: {scheme['bg']}; border-radius: 6px; }}
    .confusion-q {{ font-size: 15px; font-weight: 600; color: {scheme['secondary']}; margin-bottom: 6px; }}
    .confusion-a {{ font-size: 14px; color: {scheme['text_main']}; line-height: 1.8; }}
    .test-item {{ margin-bottom: 16px; padding: 16px 20px; background: {scheme['test_bg']}; border-radius: 8px; border: 1px solid {scheme['test_border']}; }}
    .test-q {{ font-size: 15px; font-weight: 600; color: {scheme['primary']}; margin-bottom: 8px; }}
    .test-q::before {{ content: '自测: '; color: {scheme['accent']}; }}
    .test-a {{ font-size: 14px; color: {scheme['text_secondary']}; line-height: 1.8; padding-top: 8px; border-top: 1px dashed {scheme['border']}; margin-top: 8px; }}
    .test-a::before {{ content: '参考答案: '; font-weight: 600; color: {scheme['accent']}; }}
    .source-item {{ margin-bottom: 10px; padding-left: 16px; position: relative; font-size: 14px; line-height: 1.7; }}
    .source-item::before {{ content: ''; position: absolute; left: 0; top: 10px; width: 6px; height: 6px; border-radius: 50%; background: {scheme['accent']}; }}
    .source-item a {{ color: {scheme['source_link']}; text-decoration: underline; text-underline-offset: 3px; }}
    .source-note {{ color: {scheme['highlight']}; font-size: 13px; margin-left: 8px; }}
    .footer {{ margin-top: 36px; padding-top: 16px; border-top: 1px solid {scheme['border']}; font-size: 12px; color: {scheme['highlight']}; text-align: center; }}"""


def generate_html(data, scheme):
    """生成完整HTML学习资料"""
    concept = data.get("concept", "")
    concept_zh = data.get("concept_zh", "")
    subtitle = data.get("subtitle", "")
    objectives = data.get("learning_objectives", [])
    questions = data.get("core_questions", [])
    explanation = data.get("explanation", {})
    scenario = data.get("application_scenario", {})
    confusions = data.get("confusion_points", [])
    tests = data.get("self_test", [])
    sources = data.get("sources", [])

    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="zh-CN">')
    parts.append("<head>")
    parts.append('  <meta charset="UTF-8"/>')
    parts.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>')
    parts.append(f"  <title>{escape_html(concept)} - 概念学习资料</title>")
    parts.append("  <style>")
    parts.append(generate_css(scheme))
    parts.append("  </style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append('  <div class="container">')

    # Header
    parts.append('    <div class="header">')
    parts.append(f'      <div class="header-concept">{escape_html(concept)}<span class="header-concept-zh">{escape_html(concept_zh)}</span></div>')
    parts.append(f'      <div class="header-subtitle">{escape_html(subtitle)}</div>')
    parts.append('    </div>')

    # Learning Objectives
    if objectives:
        parts.append('    <div class="objectives">')
        parts.append(f'      <div class="objectives-title">学习目标</div>')
        parts.append('      <ul>')
        for obj in objectives:
            parts.append(f'        <li>{escape_html(obj)}</li>')
        parts.append('      </ul>')
        parts.append('    </div>')

    # Core Questions
    if questions:
        parts.append('    <div class="core-questions">')
        for q in questions:
            parts.append(f'      <div class="core-question">{escape_html(q)}</div>')
        parts.append('    </div>')

    # Explanation Section
    parts.append('    <div class="section">')
    parts.append(f'      <div class="section-title">概念解释</div>')

    interpretation = explanation.get("personal_interpretation", "")
    if interpretation:
        parts.append(f'      <div class="interpretation">{escape_html(interpretation)}</div>')

    mechanisms = explanation.get("core_mechanisms", [])
    if mechanisms:
        parts.append('      <div class="mechanism-list">')
        for m in mechanisms:
            title = m.get("title", "")
            desc = m.get("description", "")
            parts.append(f'        <div class="mechanism-item">')
            parts.append(f'          <div class="mechanism-title">{escape_html(title)}</div>')
            parts.append(f'          <div class="mechanism-desc">{escape_html(desc)}</div>')
            parts.append(f'        </div>')
        parts.append('      </div>')

    features = explanation.get("key_features", [])
    if features:
        parts.append('      <div class="features">')
        for f in features:
            parts.append(f'        <span class="feature-tag">{escape_html(f)}</span>')
        parts.append('      </div>')

    parts.append('    </div>')

    # Application Scenario
    if scenario:
        parts.append('    <div class="section">')
        parts.append(f'      <div class="section-title">应用场景</div>')
        parts.append('      <div class="scenario">')
        scenario_title = scenario.get("title", "")
        if scenario_title:
            parts.append(f'        <div class="scenario-title">{escape_html(scenario_title)}</div>')
        context = scenario.get("context", "")
        if context:
            parts.append(f'        <div class="scenario-context">{escape_html(context)}</div>')
        analysis = scenario.get("analysis", "")
        if analysis:
            parts.append(f'        <div class="scenario-analysis">{escape_html(analysis)}</div>')
        parts.append('      </div>')
        parts.append('    </div>')

    # Confusion Points
    if confusions:
        parts.append('    <div class="section">')
        parts.append(f'      <div class="section-title">概念辨析</div>')
        for cp in confusions:
            q = cp.get("question", "")
            a = cp.get("clarification", "")
            parts.append(f'      <div class="confusion-item">')
            parts.append(f'        <div class="confusion-q">{escape_html(q)}</div>')
            parts.append(f'        <div class="confusion-a">{escape_html(a)}</div>')
            parts.append(f'      </div>')
        parts.append('    </div>')

    # Self Test
    if tests:
        parts.append('    <div class="section">')
        parts.append(f'      <div class="section-title">自测检验</div>')
        for t in tests:
            q = t.get("question", "")
            a = t.get("answer", "")
            parts.append(f'      <div class="test-item">')
            parts.append(f'        <div class="test-q">{escape_html(q)}</div>')
            parts.append(f'        <div class="test-a">{escape_html(a)}</div>')
            parts.append(f'      </div>')
        parts.append('    </div>')

    # Sources
    if sources:
        parts.append('    <div class="section">')
        parts.append(f'      <div class="section-title">参考来源</div>')
        for s in sources:
            title = s.get("title", "")
            url = s.get("url", "")
            note = s.get("note", "")
            parts.append(f'      <div class="source-item">')
            if url:
                parts.append(f'        <a href="{escape_html(url)}" target="_blank" rel="noopener">{escape_html(title)}</a>')
            else:
                parts.append(f'        <span>{escape_html(title)}</span>')
            if note:
                parts.append(f'        <span class="source-note">- {escape_html(note)}</span>')
            parts.append(f'      </div>')
        parts.append('    </div>')

    # Footer
    scheme_name = scheme.get("name", "")
    parts.append(f'    <div class="footer">概念学习资料 | 配色: {escape_html(scheme_name)}</div>')
    parts.append('  </div>')
    parts.append("</body>")
    parts.append("</html>")

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="概念学习资料HTML生成器")
    parser.add_argument("--input", required=True,
                        help="学习资料JSON结构字符串")
    parser.add_argument("--output", required=True,
                        help="输出HTML文件路径")
    args = parser.parse_args()

    try:
        data = json.loads(args.input)
    except json.JSONDecodeError as e:
        result = {"status": "error", "message": f"JSON解析失败: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    if "concept" not in data:
        result = {"status": "error", "message": "JSON必须包含concept字段"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    scheme_name = data.get("color_scheme", "deep_ocean")
    scheme = COLOR_SCHEMES.get(scheme_name, COLOR_SCHEMES["deep_ocean"])

    html_content = generate_html(data, scheme)

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)

        result = {
            "status": "success",
            "message": "学习资料生成成功",
            "output_path": args.output,
            "concept": data.get("concept", ""),
            "color_scheme": scheme_name,
            "scheme_display_name": scheme["name"],
            "sections": {
                "objectives": len(data.get("learning_objectives", [])),
                "mechanisms": len(data.get("explanation", {}).get("core_mechanisms", [])),
                "confusion_points": len(data.get("confusion_points", [])),
                "self_test": len(data.get("self_test", [])),
                "sources": len(data.get("sources", []))
            }
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        result = {"status": "error", "message": f"文件写入失败: {str(e)}"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
