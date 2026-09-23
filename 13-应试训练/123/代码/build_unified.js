/* build_unified.js — 全量扫描 123 下所有题库源，归一化 + 按 id/题面去重，
 * 生成 123/题库-汇总.js（window.LBLB_UNIFIED = {extras, byCat, sources, total, builtAt}）。
 * extras = 除 真题卷.js(LBLB_EXAMS.questions) 已含题目之外的全部唯一题。
 * 用法：node build_unified.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const ROOT = path.resolve(__dirname, '..'); // 123

function loadJs(file){
  const code = fs.readFileSync(file,'utf8');
  const sandbox = {window:{}, console};
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, {filename:file});
  return sandbox.window;
}
const CATMAP = {"CMC":"cmc","考研":"kaoyan","练习题":"exercise","专升本":"zsb"};
const DIFFMAP = {1:"简单",2:"比较简单",3:"基础",4:"比较难",5:"难"};

function normQ(raw, fallback){
  if(!raw || typeof raw!=='object') return null;
  const id = raw.id || raw.ID || raw._id || null;
  let cat = raw.cat || raw.category || (fallback&&fallback.cat) || 'exercise';
  if(typeof cat==='string' && CATMAP[cat]) cat = CATMAP[cat];
  const q = raw.q || raw.stem || raw.question || raw.title || '';
  let o = raw.o || raw.options || raw.choices || [];
  if(!Array.isArray(o)) o=[];
  let a = (raw.a===undefined||raw.a===null) ? -1 : raw.a;
  if(o.length<2) a=-1;
  const answer = raw.answer!==undefined ? raw.answer : (raw.ans!==undefined?raw.ans:(typeof raw.correct==='string'?raw.correct:''));
  const s = raw.s || raw.solution || raw.analysis || raw.explanation || '';
  const topic = raw.topic || raw.knowledge_point || raw.tag || raw.chapter || '';
  let difficulty = raw.difficulty;
  if(typeof difficulty==='number') difficulty = DIFFMAP[difficulty]||''; else difficulty = difficulty||'';
  let source=raw.source, sourceUrl=raw.sourceUrl||raw.url||'';
  if(source && typeof source==='object'){ sourceUrl=sourceUrl||source.url||''; source=source.title||source.name||''; }
  const type = raw.type || (o.length>=2?'choice':'calc');
  const score = raw.score || 10;
  const sub = raw.sub || raw.tag || '';
  if(!id && !q) return null;
  const kid = id || ('q-'+require('crypto').createHash('md5').update(String(q)).digest('hex').slice(0,12));
  return {id:kid, cat, sub, topic, skill:raw.skill||raw.chapter||'', source:source||'', sourceUrl,
    difficulty, q:String(q), o, a, answer:String(answer||''), s:String(s||''), score, type};
}

// 1) seeds from 真题卷.js
const wMain = loadJs(path.join(ROOT,'真题卷.js'));
const EX = wMain.LBLB_EXAMS||{};
const seeds = EX.questions||[];
const seen = new Set(seeds.map(q=>q.id));
const sources = [];
sources.push({file:'真题卷.js', count:seeds.length});

// 2) walk all live bank .js
function walk(dir,list){
  let e; try{e=fs.readdirSync(dir,{withFileTypes:true});}catch(_){return;}
  for(const x of e){
    const f=path.join(dir,x.name);
    if(x.isDirectory()){ if(x.name==='代码'||x.name==='assets') continue; walk(f,list); continue; }
    if((path.extname(x.name)||'').toLowerCase()!=='.js') continue;
    if(x.name==='题库-汇总.js') continue;
    list.push(f);
  }
}
const allJs=[]; walk(ROOT,allJs);
const extras=[]; const byCat={}; const srcLog=[];
function add(q, src){ if(!q) return; if(seen.has(q.id)) return; seen.add(q.id); extras.push(q); byCat[q.cat]=(byCat[q.cat]||0)+1; }
for(const f of allJs){
  const rel = path.relative(ROOT,f).replace(/\\/g,'/');
  const w = loadJs(f);
  const batches=[];
  if(w.QUESTION_BANK && w.QUESTION_BANK.questions) batches.push({arr:w.QUESTION_BANK.questions,cat:null,tag:rel+'/QUESTION_BANK'});
  if(Array.isArray(w.LBLB_QUIZ)) batches.push({arr:w.LBLB_QUIZ,cat:'quiz',tag:rel+'/LBLB_QUIZ'});
  if(Array.isArray(w.LBLB_CMC_REAL)) batches.push({arr:w.LBLB_CMC_REAL,cat:'real',tag:rel+'/LBLB_CMC_REAL'});
  if(Array.isArray(w.LBLB_FDU_REAL)) batches.push({arr:w.LBLB_FDU_REAL,cat:'real',tag:rel+'/LBLB_FDU_REAL'});
  if(Array.isArray(w.LBLB_ZSB_REAL)) batches.push({arr:w.LBLB_ZSB_REAL,cat:'real',tag:rel+'/LBLB_ZSB_REAL'});
  for(const b of batches){
    let added=0;
    for(const raw of b.arr){ const q=normQ(raw,{cat:b.cat}); const before=extras.length; add(q,b.tag); if(extras.length>before) added++; }
    srcLog.push({file:rel, kind:b.tag, raw:b.arr.length, added});
  }
}

const out = {
  version: (EX.version||'2026-09-18')+'-unified',
  builtAt: new Date().toISOString(),
  papers: (EX.papers||[]).length,
  seedQuestions: seeds.length,
  extraQuestions: extras.length,
  byCat: byCat,
  sources: srcLog,
  extras: extras
};
const header = '/* LBLB 统一题库（构建产物，勿手改）· 由 代码/build_unified.js 扫描 123 全部题库源生成\n'
  + ' * 种子=真题卷.js(LBLB_EXAMS.questions ' + seeds.length + ' 题, ' + (EX.papers||[]).length + ' 卷)\n'
  + ' * extras=按 id/题面去重后并入的额外题目 ' + extras.length + ' 题；byCat=' + JSON.stringify(byCat) + '\n'
  + ' * 加载后 06 单题库 = 种子 + extras。\n'
  + ' */\nwindow.LBLB_UNIFIED=';
fs.writeFileSync(path.join(ROOT,'题库-汇总.js'), header + JSON.stringify(Object.assign({},out,{extras:extras})) + ';\n', 'utf8');

console.log('papers:', (EX.papers||[]).length);
console.log('seed questions:', seeds.length);
console.log('extras:', extras.length);
console.log('total unique:', seeds.length+extras.length);
console.log('byCat:', JSON.stringify(byCat));
console.log('written:', path.join(ROOT,'题库-汇总.js'));
console.log('size KB:', (fs.statSync(path.join(ROOT,'题库-汇总.js')).size/1024).toFixed(0));
