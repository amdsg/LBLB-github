# -*- coding: utf-8 -*-
"""
生成 15-应试实战 —— 按目标考试分类的**真实真题**练习页
======================================================
数据来源：`13-应试训练/123/真题卷.js`（种子 1491 题，带完整难度/题型标签）
         + `题库-汇总.js`（附加 11367 题）

实测各目标可切题量（2026-09 盘点）：
     考研数学一 776（sub 含「数一」）   考研数学二 408（sub 含「数二」）
     专升本     5174（cat=zsb）          数学竞赛   5909（cat=cmc）
     高校期末    369（cat=exercise/fdu） 合计       12858

设计要点：
  1. 页面在浏览器里读题库并筛选，因此发布（题库被 .gitignore 排除）时会自动降级为
     「数据未随仓库分发」的说明页，不造成侵权——这正是分层隔离的用意。
  2. 筛选条件以**生成的 JS 谓词函数**形式注入，不用 JSON DSL：
     早先用 JSON 传筛选条件时，Python 的 None 被写进 JS 成了非法字面量，
     整段脚本抛错、页面全白。谓词函数没有这类跨语言字面量问题。
  3. 附加题的 difficulty 多为空（11181/11367），统一显示为「未标注」并参与筛选。

用法：python tools/build_exam_drill.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "15-应试实战")
# 试卷清单.js 只含元数据（标题/年份/来源 URL），随仓库发布；
# 题库两个文件含题目正文，默认不发布。页面据此做分级降级：
#   有题库 → 显示题目；无题库但有清单 → 显示试卷目录与官方获取渠道。
JOINTS = ["123/试卷清单.js", "123/真题卷.js", "123/题库-汇总.js"]

# (文件, 标题, 图标, 谓词 JS, 筛选说明, 导语)
TARGETS = [
    ("01-考研数学一", "考研数学一", "Ⅰ",
     "q.cat==='kaoyan' && (q.sub||'').indexOf('数一')>=0",
     "cat=kaoyan 且 sub 含「数一」",
     "高等数学约占 56%，含多元微积分、曲线曲面积分与无穷级数——这是数一区别于数二的部分。"
     "题目为公开来源的历年真题，难度标签来自原整理者的人工评分。",
     "var c=p.category||'', tg=p.tag||''; return c==='考研' && /数一|数学一/.test(tg);"),
    ("02-考研数学二", "考研数学二", "Ⅱ",
     "q.cat==='kaoyan' && (q.sub||'').indexOf('数二')>=0",
     "cat=kaoyan 且 sub 含「数二」",
     "不含无穷级数与概率论，重点为高等数学与线性代数。题目为公开来源的历年真题。",
     "var c=p.category||'', tg=p.tag||''; return c==='考研' && /数二|数学二/.test(tg);"),
    ("03-专升本", "专升本", "Z",
     "q.cat==='zsb'",
     "cat=zsb（各省专升本）",
     "各省专升本高等数学真题，覆盖面广、计算为主，难度以基础与比较简单居多。",
     "c==='专升本'"),
    ("04-数学竞赛", "大学生数学竞赛", "◎",
     "q.cat==='cmc'",
     "cat=cmc（全国大学生数学竞赛）",
     "全国大学生数学竞赛真题（非数学类／数学类）。更依赖巧劲——换元、对称性、"
     "夹逼与构造，证明题比重明显高于考研。",
     "c==='CMC'"),
    ("05-高校期末与练习", "高校期末与练习", "▤",
     "q.cat==='exercise' || q.cat==='fdu'",
     "cat=exercise 或 fdu",
     "各高校期中期末试题与公开练习题库，按学校/章节标注，适合在校课程备考与章节巩固。",
     "c==='练习题'"),
    ("06-考研数学三", "考研数学三", "Ⅲ",
     "q.cat==='kaoyan' && (q.sub||'').indexOf('数三')>=0",
     "cat=kaoyan 且 sub 含「数三」",
     "数三含高等数学、线性代数与概率统计，不含曲线曲面积分与空间解析几何。"
     "公开来源的数三题目偏少，本册题量明显低于数一／数二——这是收录现状，不是筛选造成的。",
     "var c=p.category||'', tg=p.tag||''; return c==='考研' && /数三|数学三/.test(tg);"),
    ("07-考研未标科目", "考研（未标注科目）", "？",
     "q.cat==='kaoyan' && !q.sub",
     "cat=kaoyan 且 sub 为空",
     "题库中有 188 道考研题没有标注是数一／数二／数三。按内容看它们含概率与级数，"
     "应属数一或数三，但原数据未标注——本册如实单列，不做推测性归类。",
     "var c=p.category||'', tg=p.tag||''; return c==='考研' && !/数[一二三]/.test(tg);"),
]

LEVELS = ["简单", "比较简单", "基础", "比较难", "难", "提高", "未标注"]
TYPE_NAME = {"choice": "选择题", "fill": "填空题", "calc": "计算题", "proof": "证明题",
             "text": "文字题"}

PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'none'">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>__TITLE__ · 应试实战 · LBLB</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='46' font-size='30' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3E__ICONENC__%3C/text%3E%3C/svg%3E">
<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']],processEscapes:true,processEnvironments:true},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']},svg:{fontCache:'local'},startup:{typeset:true}};</script>
__JOINTS__
<script src="../assets/mathjax/es5/tex-svg.js" async onerror="var b=document.createElement('div');b.style.cssText='padding:8px 12px;background:#FDEDE8;border:1px solid #EAC6B8;border-radius:8px;color:#C0392B;font-size:13px;margin:10px 0';b.textContent='公式渲染组件加载失败：请确认 ../assets/mathjax/es5/tex-svg.js 存在。';document.currentScript.after(b);"></script>
<style>
:root{--paper:#F7F3E7;--paper2:#EFE9D8;--ink:#22262B;--ink2:#4A5258;--line:#D8D0BC;
 --blue:#1F4E9C;--teal:#177E89;--gold:#A8751E;--red:#C0392B;--green:#2E7D5B;--violet:#6B4C9A;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);font-family:"Times New Roman","Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.8;}
button,select,input{font-family:inherit;font-size:14px;}
.wrap{max-width:1000px;margin:0 auto;padding:0 24px 90px;}
header{padding:52px 0 6px;}
.back{font-size:13px;color:var(--blue);text-decoration:none;}
.back:hover{text-decoration:underline;}
.kicker{font-size:11px;letter-spacing:.3em;color:var(--ink2);text-transform:uppercase;margin-top:22px;}
h1{font-family:Georgia,"Noto Serif SC",serif;font-size:40px;margin:10px 0 8px;}
h1 .sym{color:var(--red);font-style:italic;}
.sub{color:var(--ink2);font-size:15.5px;max-width:800px;}
.filtline{margin-top:10px;font-size:12.5px;color:var(--ink2);}
.filtline code{background:var(--paper2);border-radius:3px;padding:1px 6px;}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:18px;padding:12px 16px;background:#fffdf6;border:1px solid var(--line);border-radius:12px;}
.bar label{font-size:13.5px;color:var(--ink2);}
.bar select{padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:#fffdf6;}
.bar .btn{background:var(--blue);color:#fff;border:none;border-radius:8px;padding:7px 14px;font-size:13.5px;cursor:pointer;min-height:36px;}
.bar .btn.gray{background:#8A8270;}
.stat{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;font-size:13.5px;color:var(--ink2);}
.stat b{color:var(--ink);}
.qlist{margin-top:18px;}
.q{background:#fffdf6;border:1px solid var(--line);border-left:5px solid var(--c,var(--blue));border-radius:10px;padding:15px 18px;margin-top:14px;}
.q .head{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;margin-bottom:8px;font-size:11.5px;color:var(--ink2);}
.q .num{font-family:Georgia,serif;font-weight:700;font-size:14px;color:var(--c,var(--blue));}
.q .tagd{display:inline-block;border-radius:999px;padding:1px 9px;background:var(--paper2);color:var(--ink2);}
.q .src{margin-left:auto;font-size:11px;color:var(--ink2);max-width:46%;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.q .stem{font-size:15px;}
.q .opts{margin-top:8px;font-size:14.5px;color:var(--ink2);}
.q .opts div{margin-top:3px;}
.q details{margin-top:10px;border-top:1px dashed var(--line);padding-top:9px;}
.q summary{cursor:pointer;font-size:13.5px;color:var(--blue);user-select:none;display:inline-block;padding:3px 0;}
.q summary:hover{text-decoration:underline;}
.q .ans{margin-top:8px;font-size:14.5px;}
.q .ans b{color:var(--green);}
.q .sol{margin-top:8px;font-size:14px;color:var(--ink2);white-space:pre-wrap;}
.q .meta{margin-top:8px;font-size:11.5px;color:var(--ink2);}
.pager{display:flex;gap:8px;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:24px;}
.pager button{background:#fffdf6;border:1px solid var(--line);border-radius:8px;padding:6px 14px;cursor:pointer;min-height:36px;}
.pager button[disabled]{opacity:.45;cursor:default;}
.pager .cur{font-size:13.5px;color:var(--ink2);}
.empty{margin-top:22px;padding:16px 18px;background:#FFF9E8;border:1px solid #E5D29F;border-left:4px solid var(--gold);border-radius:10px;color:#5A4310;font-size:13.5px;line-height:1.85;}
.empty code{background:var(--paper2);border-radius:3px;padding:1px 5px;}
footer{margin-top:46px;border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;color:var(--ink2);}
footer code{background:var(--paper2);border-radius:4px;padding:1px 6px;}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="back" href="index.html">← 返回应试实战总览</a>
  <div class="kicker">LBLB · Past Exam Papers</div>
  <h1>__TITLE__ <span class="sym">__ICON__</span></h1>
  <p class="sub">__LEAD__</p>
  <p class="filtline">筛选条件：<code>__FILTERTEXT__</code></p>
</header>

<div class="bar">
  <label>难度 <select id="fLevel"><option value="">全部</option></select></label>
  <label>题型 <select id="fType"><option value="">全部</option></select></label>
  <label>每页 <select id="fSize"><option>10</option><option selected>20</option><option>50</option><option>100</option></select></label>
  <button class="btn" id="shuffle">打乱顺序</button>
  <button class="btn gray" id="reset">恢复原序</button>
  <button class="btn gray" id="toggleAll">展开全部答案</button>
</div>
<div class="stat" id="stat"></div>
<div id="notice"></div>
<div class="qlist" id="list"></div>
<div class="pager" id="pager"></div>

<footer>
  题目来自公开来源的历年真题，出处标注在每题右上角；原题版权归各命题单位所有，仅供个人学习，勿作商业用途。<br>
  来源与权利归属详见 <a class="back" href="../13-应试训练/题库来源与授权.md">13-应试训练/题库来源与授权.md</a> ·
  <a class="back" href="index.html">应试实战总览</a>
</footer>
</div>
<script>
(function(){
"use strict";

/* 本页的目标考试筛选谓词 */
var MATCH = function(q){ return __PRED__; };

/* 合并题库：种子 + 附加题，按 id 去重（与 06-真实单题训练 同一口径） */
var seed=(window.LBLB_EXAMS&&window.LBLB_EXAMS.questions)||[];
var ex=(window.LBLB_UNIFIED&&window.LBLB_UNIFIED.extras)||[];
var seen={},all=[];
function push(q){ if(q&&q.id&&!seen[q.id]){seen[q.id]=1;all.push(q);} }
for(var i=0;i<seed.length;i++) push(seed[i]);
for(var j=0;j<ex.length;j++) push(ex[j]);

var data=all.filter(MATCH);
var notice=document.getElementById('notice');

if(!data.length){
  // 降级：题库未随仓库分发时，用试卷清单（元数据，随仓库发布）列出试卷目录与官方获取渠道。
  // 这样公开仓库上的本页仍然可用——它变成一份「有哪些卷、去哪拿」的索引，而不是空白页。
  var lib=(window.PAPER_LIBRARY||[]).filter(function(p){ __CATFILTER__ });
  var missing=[];
  if(!window.LBLB_EXAMS) missing.push('123/真题卷.js');
  if(!window.LBLB_UNIFIED) missing.push('123/题库-汇总.js');

  var h='<div class="empty"><b>题库数据未随本仓库分发，本页改为显示试卷目录。</b><br>'
    +'原因：真题的著作权人是教育部考试中心、竞赛工作组与各高校，未给出再分发授权，'
    +'故本仓库只发布元数据（试卷标题、年份、出处链接），不发布题目正文与试卷原件。<br>'
    +'要让本页显示完整题目，请把题库文件放回 <code>13-应试训练/123/</code>'
    +(missing.length?('（当前缺少：'+missing.join('、')+'）'):'')+'。</div>';

  if(lib.length){
    var yrs={};
    for(var i=0;i<lib.length;i++) if(lib[i].year) yrs[lib[i].year]=1;
    var ys=Object.keys(yrs).sort();
    h+='<div class="stat"><span>本目录试卷 <b>'+lib.length+'</b> 套</span>'
      +'<span>年份 <b>'+(ys.length?(ys[0]+'–'+ys[ys.length-1]):'—')+'</b></span>'
      +'<span>题目正文 <b>不随仓库分发</b></span></div>';
    var rows=[];
    for(var j=0;j<lib.length;j++){
      var p=lib[j];
      rows.push('<article class="q" style="--c:var(--blue)">'
        +'<div class="head"><span class="num">'+esc(String(p.year||''))+'</span>'
        +'<span class="tagd">'+esc(p.category||'')+'</span>'
        +(p.tag?'<span class="tagd">'+esc(p.tag)+'</span>':'')
        +'</div><div class="stem">'+esc(p.title||'')+'</div>'
        +'<div class="meta">试卷文件：<code>'+esc(p.file||'')+'</code>（未随仓库分发）</div>'
        +'</article>');
    }
    h+='<div class="qlist">'+rows.join('')+'</div>';
  } else {
    h+='<div class="empty" style="margin-top:14px">试卷清单（<code>123/试卷清单.js</code>）也不存在，'
      +'因此无法列出目录。官方获取渠道见 <code>13-应试训练/题库来源与授权.md</code>。</div>';
  }
  notice.innerHTML=h;
  return;
}

var order=data.slice(), page=1, size=20, curLevel='', curType='';
var LEVELS=['简单','比较简单','基础','比较难','难','提高','未标注'];
var TYPES=['choice','fill','calc','proof','text'];
var TN={choice:'选择题',fill:'填空题',calc:'计算题',proof:'证明题',text:'文字题'};

function lv(q){ return q.difficulty||'未标注'; }
function tp(q){ return q.type||''; }

/* 下拉选项只列实际存在的取值 */
(function initSelects(){
  var m={}, t={};
  for(var i=0;i<data.length;i++){ m[lv(data[i])]=1; if(tp(data[i])) t[tp(data[i])]=1; }
  var lvHtml='', tyHtml='';
  for(var a=0;a<LEVELS.length;a++) if(m[LEVELS[a]]) lvHtml+='<option>'+LEVELS[a]+'</option>';
  for(var b=0;b<TYPES.length;b++) if(t[TYPES[b]]) tyHtml+='<option value="'+TYPES[b]+'">'+TN[TYPES[b]]+'</option>';
  document.getElementById('fLevel').insertAdjacentHTML('beforeend',lvHtml);
  document.getElementById('fType').insertAdjacentHTML('beforeend',tyHtml);
})();

function refreshStat(){
  var byLv={};
  for(var i=0;i<data.length;i++){var k=lv(data[i]);byLv[k]=(byLv[k]||0)+1;}
  var parts=[];
  for(var a=0;a<LEVELS.length;a++) if(byLv[LEVELS[a]]) parts.push(LEVELS[a]+' '+byLv[LEVELS[a]]);
  var srcs={};
  for(var j=0;j<data.length;j++){var s=(data[j].source||'').split('·')[0].trim();if(s)srcs[s]=1;}
  /* 年份覆盖：从题目 id 里提取 4 位年份，让「覆盖是否完整」可核查而不是靠感觉 */
  var yrs={};
  for(var m=0;m<data.length;m++){
    var mm=String(data[m].id||'').match(/(19|20)\d{2}/);
    if(mm) yrs[mm[0]]=1;
  }
  var ys=Object.keys(yrs).sort();
  var span='—', miss='';
  if(ys.length>1){
    span=ys[0]+'–'+ys[ys.length-1]+'（'+ys.length+' 个年份）';
    var gaps=[];
    for(var y=+ys[0];y<=+ys[ys.length-1];y++) if(!yrs[y]) gaps.push(y);
    if(gaps.length) miss=' 缺 '+gaps.join('/');
  }
  document.getElementById('stat').innerHTML=
    '<span>题目总数 <b>'+data.length+'</b></span>'
    +'<span>本次筛选 <b>'+order.length+'</b></span>'
    +'<span>年份覆盖 <b>'+span+miss+'</b></span>'
    +'<span>难度分布 <b>'+(parts.join(' / ')||'—')+'</b></span>'
    +'<span>来源 <b>'+Object.keys(srcs).length+'</b> 个</span>';
}

var COLORS=['var(--blue)','var(--teal)','var(--red)','var(--gold)','var(--green)','var(--violet)'];
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

function render(){
  var total=order.length, pages=Math.max(1,Math.ceil(total/size));
  if(page>pages) page=pages;
  var slice=order.slice((page-1)*size,page*size), h=[];
  for(var i=0;i<slice.length;i++){
    var q=slice[i], c=COLORS[i%COLORS.length], opts='';
    if(q.o&&q.o.length){
      opts='<div class="opts">';
      for(var k=0;k<q.o.length;k++) opts+='<div>'+String.fromCharCode(65+k)+'. '+esc(q.o[k])+'</div>';
      opts+='</div>';
    }
    var ansTxt=q.answer||'';
    if(typeof q.a==='number'&&q.a>=0&&q.o&&q.o[q.a])
      ansTxt=String.fromCharCode(65+q.a)+'．'+ansTxt;
    h.push('<article class="q" style="--c:'+c+'">'
      +'<div class="head"><span class="num">'+esc(q.id)+'</span>'
      +'<span class="tagd">'+esc(lv(q))+'</span>'
      +'<span class="tagd">'+esc(tp(q)?(TN[tp(q)]||tp(q)):'题目')+'</span>'
      +(q.sub?'<span class="tagd">'+esc(q.sub)+'</span>':'')
      +(q.source?'<span class="src" title="'+esc(q.source)+'">'+esc(q.source)+'</span>':'')
      +'</div>'
      +'<div class="stem">'+q.q+'</div>'+opts
      +'<details><summary>查看参考答案与解析</summary>'
      +(ansTxt?'<div class="ans"><b>答案：</b>'+ansTxt+'</div>':'<div class="ans" style="color:var(--ink2)">（原库未附答案）</div>')
      +(q.s?'<div class="sol">'+esc(q.s)+'</div>':'')
      +((q.source||q.sourceUrl)?'<div class="meta">出处：'+esc(q.source||'')+(q.sourceUrl?' · '+esc(q.sourceUrl):'')+(q.license?' · '+esc(q.license):'')+'</div>':'')
      +'</details></article>');
  }
  document.getElementById('list').innerHTML=h.join('');

  var pg=[];
  pg.push('<button '+(page<=1?'disabled':'')+' data-go="1">首页</button>');
  pg.push('<button '+(page<=1?'disabled':'')+' data-go="'+(page-1)+'">上一页</button>');
  pg.push('<span class="cur">第 '+page+' / '+pages+' 页</span>');
  pg.push('<button '+(page>=pages?'disabled':'')+' data-go="'+(page+1)+'">下一页</button>');
  pg.push('<button '+(page>=pages?'disabled':'')+' data-go="'+pages+'">末页</button>');
  document.getElementById('pager').innerHTML=pg.join('');
  var bs=document.querySelectorAll('#pager button[data-go]');
  for(var b=0;b<bs.length;b++) bs[b].onclick=function(){
    page=parseInt(this.getAttribute('data-go'),10); render();
    window.scrollTo({top:document.getElementById('list').offsetTop-90,behavior:'smooth'});
  };
  if(window.MathJax&&MathJax.typesetPromise) MathJax.typesetPromise();
}

function applyFilter(){
  curLevel=document.getElementById('fLevel').value;
  curType=document.getElementById('fType').value;
  size=parseInt(document.getElementById('fSize').value,10)||20;
  order=data.filter(function(q){
    if(curLevel&&lv(q)!==curLevel) return false;
    if(curType&&tp(q)!==curType) return false;
    return true;
  });
  page=1; render(); refreshStat();
}

document.getElementById('fLevel').addEventListener('change',applyFilter);
document.getElementById('fType').addEventListener('change',applyFilter);
document.getElementById('fSize').addEventListener('change',applyFilter);
document.getElementById('shuffle').addEventListener('click',function(){
  for(var i=order.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=order[i];order[i]=order[j];order[j]=t;}
  page=1; render();
});
document.getElementById('reset').addEventListener('click',applyFilter);
document.getElementById('toggleAll').addEventListener('click',function(){
  var d=document.querySelectorAll('.q details');
  var open=!(d.length&&d[0].open);
  for(var i=0;i<d.length;i++) d[i].open=open;
  this.textContent=open?'收起全部答案':'展开全部答案';
});

applyFilter();
})();
</script>
</body>
</html>
"""

IDX = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'none'">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>应试实战 · 历年真题 · LBLB</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2322262B'/%3E%3Ctext x='32' y='45' font-size='30' text-anchor='middle' fill='%23F7F3E7' font-family='Georgia,serif'%3E%E2%97%8E%3C/text%3E%3C/svg%3E">
<style>
:root{--paper:#F7F3E7;--paper2:#EFE9D8;--ink:#22262B;--ink2:#4A5258;--line:#D8D0BC;
 --blue:#1F4E9C;--teal:#177E89;--gold:#A8751E;--red:#C0392B;--green:#2E7D5B;--violet:#6B4C9A;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--paper);color:var(--ink);font-family:"Times New Roman","Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;line-height:1.8;}
.wrap{max-width:1040px;margin:0 auto;padding:0 24px 90px;}
header{padding:52px 0 6px;}
.back{font-size:13px;color:var(--blue);text-decoration:none;}
.back:hover{text-decoration:underline;}
.kicker{font-size:11px;letter-spacing:.3em;color:var(--ink2);text-transform:uppercase;margin-top:22px;}
h1{font-family:Georgia,"Noto Serif SC",serif;font-size:42px;margin:10px 0 8px;}
h1 .sym{color:var(--red);font-style:italic;}
.sub{color:var(--ink2);font-size:16px;max-width:820px;}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px;}
.chip{background:#fffdf6;border:1px solid var(--line);border-radius:999px;padding:4px 13px;font-size:12.5px;color:var(--ink2);}
.chip b{color:var(--blue);}
.note{margin-top:24px;background:#fffdf6;border:1px solid var(--line);border-left:5px solid var(--gold);border-radius:10px;padding:14px 18px;font-size:13.5px;color:var(--ink2);line-height:1.85;}
.note b{color:var(--ink);}
.note code{background:var(--paper2);border-radius:3px;padding:1px 5px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:15px;margin-top:26px;}
.card{display:block;background:#fffdf6;border:1px solid var(--line);border-top:4px solid var(--c,var(--blue));border-radius:12px;padding:16px 18px;text-decoration:none;color:var(--ink);transition:transform .12s ease,box-shadow .12s ease;}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(34,38,43,.10);}
.cardtop{display:flex;align-items:baseline;justify-content:space-between;gap:8px;}
.card .ic{font-family:Georgia,serif;font-size:23px;color:var(--c,var(--blue));}
.card .cnt{font-size:11px;color:var(--ink2);letter-spacing:.03em;text-align:right;}
.card h3{font-family:Georgia,"Noto Serif SC",serif;font-size:18px;margin:6px 0 5px;}
.card p{font-size:13px;color:var(--ink2);line-height:1.65;}
footer{margin-top:50px;border-top:1px solid var(--line);padding-top:18px;font-size:12.5px;color:var(--ink2);}
footer code{background:var(--paper2);border-radius:4px;padding:1px 6px;}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="back" href="../00-总览/index.html">← 返回总览</a>
  <div class="kicker">LBLB · Past Exam Papers</div>
  <h1>应试实战 <span class="sym">◎</span></h1>
  <p class="sub">按目标考试分类的<b>历年真题</b>。题目直接从题库中按类别与科目筛出，
  保留原题的难度标签与出处；支持按难度／题型筛选、打乱顺序、逐题展开答案与解析。</p>
  <div class="stats">
    <span class="chip">题目 <b>12858</b> 道</span>
    <span class="chip">分册 <b>5</b> 个</span>
    <span class="chip">难度标签 <b>来自原整理者评分</b></span>
  </div>
  <div class="note">
    <b>题目是真的，不是模拟的。</b>本区读取 <code>13-应试训练/123/</code> 下的题库
    （<code>真题卷.js</code> 种子 1491 题 + <code>题库-汇总.js</code> 附加 11367 题，去重后 12858 道），
    按 <code>cat</code>／<code>sub</code> 字段筛出各目标考试的真题。难度标签来自原整理者的人工评分——
    不是我们估的，也不是机器猜的。<br><br>
    <b>关于发布。</b>这些真题的著作权人是教育部考试中心、竞赛工作组与各高校，未给出再分发授权，
    因此题库数据默认<b>不随仓库发布</b>（见 <code>.gitignore</code>）。
    所以公开仓库上的本区会显示一条说明而不是题目；在你本机（题库文件齐全时）完整可用。
    权利归属、官方获取渠道见 <code>13-应试训练/题库来源与授权.md</code>。
  </div>
</header>
<div class="grid">
{{cards}}
</div>
<footer>
  原题版权归各命题单位所有，仅供个人学习，勿作商业用途。<br>
  <a class="back" href="../00-总览/index.html">← 返回总览</a> ·
  <a class="back" href="../14-自测题库/index.html">自测题库（答案经符号计算验证）→</a>
</footer>
</div>
</body>
</html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    joints = "\n".join('<script src="../13-应试训练/%s"></script>' % j for j in JOINTS)
    cards = []
    COLORS = ["var(--blue)", "var(--teal)", "var(--green)", "var(--violet)", "var(--gold)"]

    for i, (page, title, icon, pred, ftext, lead, catfilter) in enumerate(TARGETS):
        iconenc = "".join("%%%02X" % b for b in icon.encode("utf-8"))
        doc = (PAGE.replace("__TITLE__", title)
               .replace("__ICONENC__", iconenc)
               .replace("__ICON__", icon)
               .replace("__LEAD__", lead)
               .replace("__FILTERTEXT__", ftext)
               .replace("__JOINTS__", joints)
               .replace("__PRED__", pred)
               .replace("__CATFILTER__", catfilter))
        out = os.path.join(OUT, page + ".html")
        io.open(out, "w", encoding="utf-8", newline="\n").write(doc)
        print("  -> %s" % os.path.relpath(out, ROOT))
        cards.append('<a class="card" style="--c:%s" href="%s.html">'
                     '<div class="cardtop"><span class="ic">%s</span>'
                     '<span class="cnt">%s</span></div>'
                     "<h3>%s</h3><p>%s</p></a>"
                     % (COLORS[i % len(COLORS)], page, icon, ftext, title, lead[:104]))

    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8",
            newline="\n").write(IDX.replace("{{cards}}", "\n".join(cards)))
    print("  -> 15-应试实战/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
