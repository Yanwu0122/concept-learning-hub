#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_hub.py — 依据 catalog.json 重建知识库门户 hub.html

用法（在仓库根目录执行）:
    python .workbuddy/skills/knowledge-organizer/scripts/rebuild_hub.py

原理:
    1. 读取 learning-materials/catalog.json（数据真源，由 knowledge-organizer 维护）
    2. 把 catalog 原样内嵌到 hub.html 的 <script type="application/json"> 数据块
       （内嵌而非运行时 fetch，保证在 file:// 本地双击打开也能正常工作）
    3. 输出 learning-materials/hub.html（交互式门户：领域分区 / 搜索 / 复习）

注意:
    hub.html 的数据部分由本脚本生成，请勿手工编辑；改数据请改 catalog.json 后重跑本脚本。
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CATALOG_PATH = REPO_ROOT / "learning-materials" / "catalog.json"
OUT_PATH = REPO_ROOT / "learning-materials" / "hub.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识库门户 · Concept Learning Hub</title>
<style>
  :root{
    --bg:#f6f7fb; --card:#ffffff; --ink:#1e2430; --sub:#5b6472;
    --line:#e5e8f0; --brand:#4f46e5; --brand-soft:#eef2ff;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  body{
    font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
    background:var(--bg); color:var(--ink); line-height:1.6; padding:0 0 64px;
  }
  header.hero{
    background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 55%,#db2777 100%);
    color:#fff; padding:44px 20px 120px; text-align:center; position:relative;
  }
  header.hero h1{font-size:30px; font-weight:700; letter-spacing:.5px;}
  header.hero p{opacity:.92; margin-top:8px; font-size:15px;}
  .stats{display:flex; gap:12px; justify-content:center; margin-top:18px; flex-wrap:wrap;}
  .stat{background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.25);
        border-radius:999px; padding:4px 16px; font-size:13px;}
  .control{max-width:960px; margin:-70px auto 0; padding:0 20px; position:relative; z-index:2;}
  .searchbar{
    background:var(--card); border-radius:16px; box-shadow:0 8px 30px rgba(30,41,59,.10);
    padding:14px 18px; display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  }
  .searchbar input{
    flex:1; min-width:220px; border:none; outline:none; font-size:16px; background:transparent; color:var(--ink);
  }
  .searchbar input::placeholder{color:#98a0af;}
  .btn{
    border:none; cursor:pointer; font-size:14px; border-radius:10px; padding:8px 16px;
    background:var(--brand); color:#fff; font-weight:600; transition:.15s;
  }
  .btn:hover{filter:brightness(1.08);}
  .btn.ghost{background:var(--brand-soft); color:var(--brand);}
  .chips{display:flex; gap:8px; flex-wrap:wrap; margin-top:14px;}
  .chip{
    border:1px solid var(--line); background:var(--card); color:var(--sub);
    border-radius:999px; padding:5px 14px; font-size:13px; cursor:pointer; transition:.15s;
  }
  .chip:hover{border-color:var(--brand); color:var(--brand);}
  .chip.on{background:var(--brand); border-color:var(--brand); color:#fff; font-weight:600;}
  .count{max-width:960px; margin:18px auto 0; padding:0 20px; color:var(--sub); font-size:13px;}
  .grid{max-width:960px; margin:14px auto 0; padding:0 20px; display:grid;
        grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px;}
  .card{
    background:var(--card); border-radius:14px; overflow:hidden; cursor:pointer;
    border:1px solid var(--line); box-shadow:0 2px 10px rgba(30,41,59,.05);
    display:flex; flex-direction:column; transition:.15s; text-decoration:none; color:inherit;
  }
  .card:hover{transform:translateY(-3px); box-shadow:0 10px 26px rgba(30,41,59,.12); border-color:#c7cbe0;}
  .bar{height:6px; flex:none;}
  .card-body{padding:16px 18px 14px; display:flex; flex-direction:column; gap:8px; flex:1;}
  .card h3{font-size:17px;}
  .tags{display:flex; flex-wrap:wrap; gap:6px;}
  .tag{font-size:11px; color:var(--sub); background:#f0f2f8; border-radius:6px; padding:2px 8px;}
  .card p{font-size:13px; color:var(--sub); flex:1;}
  .card .go{font-size:13px; font-weight:600; color:var(--brand); margin-top:6px;}
  .card.overview{grid-column:1/-1; flex-direction:row; align-items:center; gap:14px;}
  .card.overview .card-body{padding:18px 22px;}
  .card.overview h3{font-size:19px;}
  .empty{grid-column:1/-1; text-align:center; color:var(--sub); padding:40px 0; font-size:15px;}
  footer{max-width:960px; margin:40px auto 0; padding:0 20px; color:#98a0af; font-size:12px; text-align:center;}
  .badge{display:inline-flex; align-items:center; gap:6px; font-size:12px; font-weight:600;
         border-radius:999px; padding:3px 10px; color:#fff;}
</style>
</head>
<body>

<header class="hero">
  <h1>🧭 知识库门户</h1>
  <p>Concept Learning Hub · 一个概念一份笔记 · 自动分类 / 一键检索 / 随机复习</p>
  <div class="stats" id="stats"></div>
</header>

<div class="control">
  <div class="searchbar">
    <input id="q" type="search" placeholder="🔍 搜索概念、标签或关键词…（如：Token / Agent / RLHF）" autocomplete="off">
    <button class="btn ghost" id="randBtn" title="随机打开一份笔记用于复习">🎲 随机复习</button>
  </div>
  <div class="chips" id="chips"></div>
</div>

<div class="count" id="count"></div>
<div class="grid" id="grid"></div>

<footer>
  数据由 <code>learning-materials/catalog.json</code> 驱动，页面由 knowledge-organizer Skill 自动重建 · 最后更新：__UPDATED__
</footer>

<script type="application/json" id="catalog-data">
__CATALOG_JSON__
</script>

<script>
(function(){
  var catalog = JSON.parse(document.getElementById('catalog-data').textContent);
  var entries = catalog.entries, domains = catalog.domains;
  var active = null, kw = '';
  var domById = {}; domains.forEach(function(d){ domById[d.id] = d; });

  // 统计
  var statHtml = '<span class="stat">📄 笔记 ' + entries.length + ' 份</span>';
  statHtml += '<span class="stat">🗂️ 领域 ' + domains.length + ' 类</span>';
  statHtml += '<span class="stat">🏷️ 标签 ' + countTags() + ' 个</span>';
  document.getElementById('stats').innerHTML = statHtml;
  function countTags(){ var s = {}; entries.forEach(function(e){ e.tags.forEach(function(t){ s[t]=1; }); }); return Object.keys(s).length; }

  // 领域 chips（含"全部"）
  var chipsEl = document.getElementById('chips');
  var chipAll = document.createElement('button');
  chipAll.className = 'chip on'; chipAll.textContent = '📂 全部领域';
  chipAll.onclick = function(){ active = null; refresh(); };
  chipsEl.appendChild(chipAll);
  domains.forEach(function(d){
    var n = entries.filter(function(e){ return e.domain === d.id; }).length;
    if (n === 0) return;
    var b = document.createElement('button');
    b.className = 'chip'; b.textContent = d.emoji + ' ' + d.name + ' (' + n + ')';
    b.onclick = function(){ active = d.id; refresh(); };
    chipsEl.appendChild(b);
  });

  var qEl = document.getElementById('q');
  qEl.addEventListener('input', function(){ kw = qEl.value.trim().toLowerCase(); refresh(); });

  document.getElementById('randBtn').onclick = function(){
    var pool = entries;
    if (pool.length === 0) return;
    var e = pool[Math.floor(Math.random() * pool.length)];
    window.open(e.file.split('/').pop(), '_blank');
  };

  function matches(e){
    if (active && e.domain !== active) return false;
    if (!kw) return true;
    var dom = domById[e.domain];
    var hay = (e.title + ' ' + e.summary + ' ' + e.tags.join(' ') + ' ' + dom.name + ' ' + dom.desc).toLowerCase();
    return hay.indexOf(kw) >= 0;
  }

  function refresh(){
    var list = entries.filter(matches);
    // overview 类型的总览卡片永远排最前
    list.sort(function(a,b){ return (a.type==='overview'?0:1) - (b.type==='overview'?0:1); });
    var grid = document.getElementById('grid');
    grid.innerHTML = '';
    document.getElementById('count').textContent = '共 ' + list.length + ' 份' + (active ? '（领域：' + domById[active].name + '）' : '') + (kw ? '，匹配关键词「' + qEl.value.trim() + '」' : '');
    if (list.length === 0){
      var e = document.createElement('div'); e.className='empty'; e.textContent='没有匹配的笔记，换个关键词试试？';
      grid.appendChild(e); return;
    }
    list.forEach(function(en){
      var dom = domById[en.domain];
      var a = document.createElement('a');
      a.className = 'card' + (en.type === 'overview' ? ' overview' : '');
      a.href = en.file.split('/').pop();
      a.target = '_blank';
      var tags = en.tags.map(function(t){ return '<span class="tag">#' + t + '</span>'; }).join('');
      a.innerHTML =
        '<div class="bar" style="background:' + dom.color + '"></div>' +
        '<div class="card-body">' +
          '<div><span class="badge" style="background:' + dom.color + '">' + dom.emoji + ' ' + dom.name + '</span></div>' +
          '<h3>' + en.title + '</h3>' +
          '<p>' + en.summary + '</p>' +
          '<div class="tags">' + tags + '</div>' +
          '<div class="go">打开笔记 →</div>' +
        '</div>';
      grid.appendChild(a);
    });
    // 更新 chips 高亮
    var allChips = chipsEl.querySelectorAll('.chip');
    allChips.forEach(function(c){
      c.classList.remove('on');
      if (!active && c.textContent.indexOf('全部') === 0) c.classList.add('on');
    });
  }

  refresh();
})();
</script>
</body>
</html>
"""


def main():
    if not CATALOG_PATH.exists():
        sys.exit(f"[error] 找不到 {CATALOG_PATH}，请在仓库根目录运行本脚本。")
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    html = TEMPLATE.replace("__CATALOG_JSON__", json.dumps(catalog, ensure_ascii=False, indent=2))
    html = html.replace("__UPDATED__", catalog.get("updated", ""))
    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"[ok] 已生成 {OUT_PATH.relative_to(REPO_ROOT)}（条目数：{len(catalog['entries'])}）")


if __name__ == "__main__":
    main()
