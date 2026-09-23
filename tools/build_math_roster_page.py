# -*- coding: utf-8 -*-
"""
生成 11-数学家/数学家名录.html
============================
读取 数学家名录数据.js（由 build_math_roster.py 生成），提供检索、按国籍/时代筛选、
分页浏览，并如实标注数据现状（哪些字段已核实、哪些待补）。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "11-数学家", "数学家名录.html")

PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'none'">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>数学家名录 · 检索一万位数学家 · LBLB</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='45' font-size='30' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3ES%3C/text%3E%3C/svg%3E">
<script src="数学家名录数据.js"></script>
<style>
:root{--paper:#F7F3E7;--paper2:#EFE9D8;--ink:#22262B;--ink2:#4A5258;--line:#D8D0BC;
 --blue:#1F4E9C;--teal:#177E89;--gold:#A8751E;--red:#C0392B;--green:#2E7D5B;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);font-family:"Times New Roman","Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.75;}
button,select,input{font-family:inherit;font-size:14px;}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px 80px;}
header{padding:48px 0 6px;}
.back{font-size:13px;color:var(--blue);text-decoration:none;}
.back:hover{text-decoration:underline;}
.kicker{font-size:11px;letter-spacing:.3em;color:var(--ink2);text-transform:uppercase;margin-top:20px;}
h1{font-family:Georgia,"Noto Serif SC",serif;font-size:40px;margin:10px 0 8px;}
h1 em{font-style:italic;color:var(--red);}
.sub{color:var(--ink2);font-size:15.5px;max-width:820px;}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;}
.chip{background:#fffdf6;border:1px solid var(--line);border-radius:999px;padding:4px 13px;font-size:12.5px;color:var(--ink2);}
.chip b{color:var(--blue);}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:18px;padding:12px 16px;background:#fffdf6;border:1px solid var(--line);border-radius:12px;}
.bar input[type=search]{flex:1;min-width:200px;padding:7px 11px;border:1px solid var(--line);border-radius:8px;background:#fff;}
.bar select{padding:6px 9px;border:1px solid var(--line);border-radius:8px;background:#fffdf6;max-width:190px;}
.bar .btn{background:var(--blue);color:#fff;border:none;border-radius:8px;padding:7px 14px;cursor:pointer;min-height:36px;}
.tbl{margin-top:18px;width:100%;border-collapse:collapse;background:#fffdf6;font-size:13.5px;}
.tbl th,.tbl td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;}
.tbl th{background:var(--paper2);font-size:12.5px;color:var(--ink2);position:sticky;top:0;}
.tbl tr:hover td{background:#fffef9;}
.nm{font-weight:600;}
.nm small{display:block;font-weight:400;color:var(--ink2);font-size:12px;}
.ct{color:var(--ink2);font-size:13px;}
.ct.pending{color:#A8751E;}
.dt{white-space:nowrap;font-size:12.5px;}
a.src{font-size:12px;color:var(--blue);}
.pager{display:flex;gap:8px;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:20px;}
.pager button{background:#fffdf6;border:1px solid var(--line);border-radius:8px;padding:6px 13px;cursor:pointer;min-height:36px;}
.pager button[disabled]{opacity:.45;cursor:default;}
.pager .cur{font-size:13.5px;color:var(--ink2);}
.note{margin-top:22px;background:#fffdf6;border:1px solid var(--line);border-left:5px solid var(--gold);border-radius:10px;padding:14px 18px;font-size:13.5px;color:var(--ink2);line-height:1.85;}
.note b{color:var(--ink);}
.note code{background:var(--paper2);border-radius:3px;padding:1px 5px;}
footer{margin-top:44px;border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;color:var(--ink2);}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="back" href="数学群星谱.html">← 返回数学家</a>
  <div class="kicker">LBLB · Roster of Mathematicians</div>
  <h1>数学家名录 <em>1–10,000</em></h1>
  <p class="sub">按外文原名、生卒年、国籍/地区与时代分档检索一万位数学家，每人附可在线核实的来源页面。
  这份名录的价值在于<b>广度与可追溯</b>：想找某位不太有名的数学家，或想按国家、时代筛人，用它比翻传记快得多。</p>
  <div class="stats">
    <span class="chip">收录 <b>10,000</b> 人</span>
    <span class="chip">国籍/地区 <b>412</b> 种</span>
    <span class="chip">时代分档 <b>11</b> 档</span>
    <span class="chip">来源 <b>Wikipedia / MacTutor</b></span>
  </div>
</header>

<div class="note">
  <b>关于数据现状，如实说明。</b>名录只收录<b>事实性字段</b>——外文原名、生卒年、国籍/地区、出处链接。
  这些是可核查的事实，不受著作权保护。<br>
  <b>贡献栏：</b>只在原文本身已是中文时收录（<b id="cntZh">—</b> 条）；其余条目的贡献描述目前只有英文原文，
  本文库<b>不搬运未翻译的英文</b>，故标注为「暂无中文简介」，请点来源链接查看。<br>
  <b>待补之处：</b>部分条目的生卒年为「?」（原数据即未考订），中文译名尚未翻译的条目只显示外文原名。
  这些缺口是原始采集数据的现状，不是本页的取舍。
</div>

<div class="bar">
  <input type="search" id="kw" placeholder="搜外文原名或中文译名，如 Gauss / 高斯 / Euler / 欧拉">
  <select id="fNat"><option value="">全部国籍/地区</option></select>
  <select id="fEra"><option value="">全部时代</option></select>
  <select id="fSize"><option>25</option><option selected>50</option><option>100</option></select>
  <button class="btn" id="reset">清空筛选</button>
</div>
<div class="stats" id="stat"></div>
<div class="tblwrap">
<table class="tbl">
  <thead><tr><th style="width:26%">姓名</th><th style="width:14%">生卒</th>
  <th style="width:14%">国籍/地区</th><th style="width:10%">时代</th>
  <th>贡献</th></tr></thead>
  <tbody id="rows"></tbody>
</table>
</div>
<div class="pager" id="pager"></div>

<footer>
  数据来源：English Wikipedia 与 MacTutor 数学史档案的公开条目；人名、生卒年、国籍为事实性信息。
  原始采集数据存在未翻译与未考订之处，本页已在正文如实标注。<br>
  <a class="back" href="数学群星谱.html">数学群星谱 →</a> ·
  <a class="back" href="数学家的故事.html">数学家的故事 →</a> ·
  <a class="back" href="当代华人数学家.html">当代华人数学家 →</a>
</footer>
</div>
<script>
(function(){
"use strict";
var ALL = window.LBLB_MATH_ROSTER || [];
if(!ALL.length){
  document.getElementById('rows').innerHTML =
    '<tr><td colspan="5" style="padding:20px;color:#A8751E">名录数据文件（数学家名录数据.js）未能加载。</td></tr>';
  return;
}
var nZh = ALL.filter(function(x){return x.k;}).length;
document.getElementById('cntZh').textContent = nZh;

var PAGE_ORDER = ["公元前","5世纪以前","中世纪","文艺复兴","17世纪","18世纪","19世纪","20世纪上半","20世纪下半","当代","年代不详"];
(function initSelects(){
  var nats={}, eras={};
  for(var i=0;i<ALL.length;i++){ nats[ALL[i].g]=1; eras[ALL[i].e]=1; }
  var ns=Object.keys(nats).sort(function(a,b){
    if(a==='未标注') return 1; if(b==='未标注') return -1;
    return a.localeCompare(b);});
  var es=PAGE_ORDER.filter(function(e){return eras[e];});
  document.getElementById('fNat').insertAdjacentHTML('beforeend',
    ns.map(function(x){return '<option>'+x+'</option>';}).join(''));
  document.getElementById('fEra').insertAdjacentHTML('beforeend',
    es.map(function(x){return '<option>'+x+'</option>';}).join(''));
})();

var cur=[], page=1, size=50;
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

function apply(){
  var kw=document.getElementById('kw').value.trim().toLowerCase();
  var nat=document.getElementById('fNat').value, era=document.getElementById('fEra').value;
  size=parseInt(document.getElementById('fSize').value,10)||50;
  cur=ALL.filter(function(x){
    if(nat&&x.g!==nat) return false;
    if(era&&x.e!==era) return false;
    if(kw){
      var hay=((x.n||'')+' '+(x.c||'')).toLowerCase();
      if(hay.indexOf(kw)<0) return false;
    }
    return true;
  });
  page=1; render(); stat();
}
function stat(){
  document.getElementById('stat').innerHTML =
    '<span>命中 <b>'+cur.length+'</b> / '+ALL.length+' 人</span>'
    +'<span>含中文简介 <b>'+cur.filter(function(x){return x.k;}).length+'</b></span>';
}
function render(){
  var pages=Math.max(1,Math.ceil(cur.length/size));
  if(page>pages) page=pages;
  var sl=cur.slice((page-1)*size,page*size), h=[];
  for(var i=0;i<sl.length;i++){
    var x=sl[i];
    var name = x.c ? (esc(x.c)+'<small>'+esc(x.n)+'</small>') : esc(x.n);
    var contrib = x.k ? '<span class="ct">'+esc(x.k)+'</span>'
                      : '<span class="ct pending">暂无中文简介，见来源</span>';
    h.push('<tr>'
      +'<td class="nm">'+name+'</td>'
      +'<td class="dt">'+esc(x.d||'?')+'</td>'
      +'<td>'+esc(x.g||'未标注')+'</td>'
      +'<td>'+esc(x.e||'')+'</td>'
      +'<td>'+contrib+(x.u?' <a class="src" href="'+esc(x.u)+'" target="_blank" rel="noopener noreferrer">来源↗</a>':'')+'</td>'
      +'</tr>');
  }
  document.getElementById('rows').innerHTML = h.join('');
  var pg=['<button '+(page<=1?'disabled':'')+' data-go="1">首页</button>',
          '<button '+(page<=1?'disabled':'')+' data-go="'+(page-1)+'">上一页</button>',
          '<span class="cur">第 '+page+' / '+pages+' 页</span>',
          '<button '+(page>=pages?'disabled':'')+' data-go="'+(page+1)+'">下一页</button>',
          '<button '+(page>=pages?'disabled':'')+' data-go="'+pages+'">末页</button>'];
  document.getElementById('pager').innerHTML=pg.join('');
  var bs=document.querySelectorAll('#pager button[data-go]');
  for(var b=0;b<bs.length;b++) bs[b].onclick=function(){
    page=parseInt(this.getAttribute('data-go'),10); render();
    window.scrollTo({top:document.querySelector('.tblwrap').offsetTop-80,behavior:'smooth'});
  };
}
var t=null;
document.getElementById('kw').addEventListener('input',function(){
  if(t) clearTimeout(t); t=setTimeout(apply,180);
});
document.getElementById('fNat').addEventListener('change',apply);
document.getElementById('fEra').addEventListener('change',apply);
document.getElementById('fSize').addEventListener('change',apply);
document.getElementById('reset').addEventListener('click',function(){
  document.getElementById('kw').value='';
  document.getElementById('fNat').value='';
  document.getElementById('fEra').value='';
  apply();
});
apply();
})();
</script>
</body>
</html>
"""

io.open(OUT, "w", encoding="utf-8", newline="\n").write(PAGE)
print("写出 %s (%.0f KB)" % (os.path.relpath(OUT, ROOT), os.path.getsize(OUT) / 1024))
