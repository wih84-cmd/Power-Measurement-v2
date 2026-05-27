import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="프로보 에너지 모니터",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  .block-container{padding-top:1.2rem;padding-bottom:1rem;max-width:1080px}
  h1{font-size:1.4rem!important;font-weight:500!important}
  footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🤖 프로보 에너지 과부하 모니터")
st.caption("3D 블록을 클릭해 모터를 설치하고, 실시간 전력·작동 시간을 확인하세요.")

components.html("""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1e293b;min-height:100vh}

.app{display:grid;grid-template-columns:1fr 300px;min-height:580px;border-radius:16px;overflow:hidden;border:1px solid #e2e8f0}

.board-panel{padding:20px;background:#fff;border-right:1px solid #e2e8f0}
.panel-title{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#64748b;margin-bottom:12px}

canvas{display:block;width:100%;cursor:pointer;border-radius:12px;background:#f1f5f9}

.palette{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.motor-btn{display:flex;align-items:center;gap:7px;padding:8px 13px;border-radius:10px;border:1.5px solid #e2e8f0;background:#fff;font-size:12px;font-weight:600;cursor:pointer;color:#334155;transition:all .15s;white-space:nowrap}
.motor-btn:hover{background:#f8fafc;transform:translateY(-1px)}
.motor-btn.sel{border-width:2px;background:#fafafe}
.dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.amps-badge{font-size:10px;color:#94a3b8;font-weight:400}
.hint{font-size:11px;color:#94a3b8;margin-top:8px;line-height:1.5}

.stats-panel{padding:18px;background:#fafafe;display:flex;flex-direction:column;gap:12px;overflow-y:auto}

.status-pill{padding:9px 13px;border-radius:10px;font-size:12px;font-weight:600;border-left:3px solid;transition:all .4s}
.s-safe  {background:#f0fdf4;color:#15803d;border-color:#22c55e}
.s-warn  {background:#fffbeb;color:#92400e;border-color:#f59e0b}
.s-danger{background:#fff1f2;color:#be123c;border-color:#ef4444}

.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sc{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 12px}
.sl{font-size:10px;color:#94a3b8;margin-bottom:3px}
.sv{font-size:19px;font-weight:600;color:#0f172a;line-height:1}
.su{font-size:10px;color:#94a3b8;font-weight:400}

.gs{display:flex;flex-direction:column;gap:4px}
.gh{display:flex;justify-content:space-between;font-size:11px;color:#64748b}
.gt{height:12px;background:#e2e8f0;border-radius:99px;overflow:hidden}
.gf{height:100%;border-radius:99px;transition:width .6s cubic-bezier(.4,0,.2,1),background .4s}

.row{display:flex;align-items:center;gap:8px;font-size:11px;color:#64748b}
.row input[type=range]{flex:1;accent-color:#6366f1;cursor:pointer}
.row b{min-width:28px;text-align:right;color:#1e293b;font-weight:600}

.time-box{text-align:center;padding:10px;background:#fff;border:1px solid #e2e8f0;border-radius:10px}
.tn{font-size:28px;font-weight:700;color:#1e293b;line-height:1}
.tl{font-size:10px;color:#94a3b8;margin-top:3px}

.bat-row{display:flex;gap:6px}
.bb{flex:1;padding:7px 4px;border:1.5px solid #e2e8f0;border-radius:9px;background:#fff;font-size:11px;font-weight:600;cursor:pointer;color:#64748b;transition:all .15s}
.bb:hover{background:#f1f5f9}
.bb.on{border-color:#6366f1;background:#eef2ff;color:#4338ca}

.legend{display:flex;flex-direction:column;gap:0}
.lr{display:flex;align-items:center;justify-content:space-between;font-size:11px;padding:5px 0;border-bottom:1px solid #f1f5f9}
.lr:last-child{border-bottom:none}
.ll{display:flex;align-items:center;gap:6px;color:#64748b}
.lv{font-weight:600;color:#0f172a}

.reset{width:100%;padding:8px;border:1px solid #e2e8f0;border-radius:9px;background:#fff;font-size:11px;font-weight:500;cursor:pointer;color:#64748b;transition:all .15s}
.reset:hover{background:#fef2f2;border-color:#fca5a5;color:#dc2626}
</style>
</head>
<body>
<div class="app">
  <div class="board-panel">
    <div class="panel-title">로봇 보드 — 셀을 클릭해 블록 설치 / 재클릭으로 제거</div>
    <canvas id="c" height="340"></canvas>
    <div class="palette">
      <button class="motor-btn sel" id="btn-m120" onclick="sel('m120')">
        <span class="dot" style="background:#22c55e"></span>120 모터<span class="amps-badge">0.4 A</span>
      </button>
      <button class="motor-btn" id="btn-m300" onclick="sel('m300')">
        <span class="dot" style="background:#ef4444"></span>300 모터<span class="amps-badge">0.8 A</span>
      </button>
      <button class="motor-btn" id="btn-servo" onclick="sel('servo')">
        <span class="dot" style="background:#3b82f6"></span>서보 모터<span class="amps-badge">0.2 A</span>
      </button>
    </div>
    <div class="hint">모터를 선택한 뒤 보드 셀을 클릭하면 3D 블록이 설치됩니다.<br>같은 셀을 다시 클릭하면 제거됩니다.</div>
  </div>

  <div class="stats-panel">
    <div id="sp" class="status-pill s-safe">✓ 안전 — 정상 작동 중</div>

    <div class="stat-grid">
      <div class="sc"><div class="sl">소모 전류</div><div class="sv"><span id="sc">0.00</span><span class="su"> A</span></div></div>
      <div class="sc"><div class="sl">소모 전력</div><div class="sv"><span id="sp2">0.0</span><span class="su"> W</span></div></div>
      <div class="sc"><div class="sl">배터리 용량</div><div class="sv"><span id="scap">2500</span><span class="su"> mAh</span></div></div>
      <div class="sc"><div class="sl">설치된 모터</div><div class="sv"><span id="scnt">0</span><span class="su"> 개</span></div></div>
    </div>

    <div class="gs">
      <div class="gh"><span>전력 부하율</span><span id="gpct">0%</span></div>
      <div class="gt"><div class="gf" id="gfill" style="width:0%;background:#22c55e"></div></div>
    </div>

    <div class="row">
      <span>최대치</span>
      <input type="range" min="1" max="60" value="15" step="1" id="maxw" oninput="upd()">
      <b id="mv">15</b><span>W</span>
    </div>

    <div class="time-box">
      <div class="tn" id="st">—</div>
      <div class="tl">예상 작동 시간</div>
    </div>

    <div>
      <div class="bat-row" style="margin-bottom:8px">
        <button class="bb on" id="bat-AA" onclick="setBat('AA')">AA  2500 mAh</button>
        <button class="bb" id="bat-AAA" onclick="setBat('AAA')">AAA  1200 mAh</button>
      </div>
      <div class="row">
        <span>팩 수</span>
        <input type="range" min="1" max="10" value="1" step="1" id="packs" oninput="upd()">
        <b id="pv">1</b><span>팩</span>
      </div>
    </div>

    <div class="legend">
      <div class="lr"><span class="ll"><span class="dot" style="width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block"></span>120 모터</span><span class="lv" id="l0">0개 — 0.0A</span></div>
      <div class="lr"><span class="ll"><span class="dot" style="width:8px;height:8px;border-radius:50%;background:#ef4444;display:inline-block"></span>300 모터</span><span class="lv" id="l1">0개 — 0.0A</span></div>
      <div class="lr"><span class="ll"><span class="dot" style="width:8px;height:8px;border-radius:50%;background:#3b82f6;display:inline-block"></span>서보 모터</span><span class="lv" id="l2">0개 — 0.0A</span></div>
    </div>

    <button class="reset" onclick="resetAll()">↺ 전체 초기화</button>
  </div>
</div>

<script>
const COLS=5,ROWS=4;
const M={
  m120:{label:'120',top:'#4ade80',side:'#15803d',dark:'#166534',amps:0.4,color:'#22c55e'},
  m300:{label:'300',top:'#f87171',side:'#b91c1c',dark:'#7f1d1d',amps:0.8,color:'#ef4444'},
  servo:{label:'SV', top:'#60a5fa',side:'#1d4ed8',dark:'#1e3a8a',amps:0.2,color:'#3b82f6'},
};
const BAT={AA:2500,AAA:1200};
let grid=Array(ROWS).fill(null).map(()=>Array(COLS).fill(null));
let chosen='m120',bat='AA',hov=null;
const cv=document.getElementById('c');
const cx=cv.getContext('2d');

function iso(c,r){
  const W=cv.width,cW=54,cH=28,ox=W/2,oy=64;
  return{x:ox+(c-r)*(cW/2),y:oy+(c+r)*(cH/2)};
}
function draw(){
  cv.width=cv.offsetWidth*devicePixelRatio||cv.offsetWidth;
  cx.clearRect(0,0,cv.width,cv.height);
  const cW=54,cH=28,bH=26;
  const gl='rgba(100,116,139,.2)';
  for(let r=ROWS-1;r>=0;r--){
    for(let c=COLS-1;c>=0;c--){
      const p=iso(c,r),hw=cW/2,hh=cH/2;
      cx.beginPath();
      cx.moveTo(p.x,p.y-hh);cx.lineTo(p.x+hw,p.y);
      cx.lineTo(p.x,p.y+hh);cx.lineTo(p.x-hw,p.y);
      cx.closePath();
      cx.fillStyle='#e2e8f0';cx.fill();
      cx.strokeStyle=gl;cx.lineWidth=.8;cx.stroke();
      if(hov&&hov.r===r&&hov.c===c&&!grid[r][c]){
        cx.fillStyle='rgba(99,102,241,.2)';cx.fill();
      }
      cx.fillStyle='#94a3b8';cx.font='500 9px system-ui';
      cx.textAlign='center';cx.textBaseline='middle';
      cx.fillText(r*COLS+c+1,p.x,p.y);
    }
  }
  for(let r=ROWS-1;r>=0;r--){
    for(let c=COLS-1;c>=0;c--){
      const m=grid[r][c];if(!m)continue;
      const mt=M[m],p=iso(c,r),hw=cW/2,hh=cH/2;
      cx.beginPath();
      cx.moveTo(p.x,p.y-hh);cx.lineTo(p.x+hw,p.y);
      cx.lineTo(p.x,p.y+hh);cx.lineTo(p.x-hw,p.y);
      cx.closePath();cx.fillStyle=mt.top;cx.fill();
      cx.beginPath();
      cx.moveTo(p.x-hw,p.y);cx.lineTo(p.x,p.y+hh);
      cx.lineTo(p.x,p.y+hh+bH);cx.lineTo(p.x-hw,p.y+bH);
      cx.closePath();cx.fillStyle=mt.dark;cx.fill();
      cx.beginPath();
      cx.moveTo(p.x+hw,p.y);cx.lineTo(p.x,p.y+hh);
      cx.lineTo(p.x,p.y+hh+bH);cx.lineTo(p.x+hw,p.y+bH);
      cx.closePath();cx.fillStyle=mt.side;cx.fill();
      cx.fillStyle='rgba(255,255,255,.9)';
      cx.font='700 9px system-ui';cx.textAlign='center';cx.textBaseline='middle';
      cx.fillText(mt.label,p.x,p.y);
      cx.fillStyle='rgba(255,255,255,.6)';
      cx.font='500 8px system-ui';
      cx.fillText(mt.amps+'A',p.x,p.y+10);
    }
  }
}
function hit(mx,my){
  const cW=54,cH=28;let best=null,bd=999;
  for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){
    const p=iso(c,r),hw=cW/2,hh=cH/2;
    const dx=mx-p.x,dy=my-p.y;
    const u=dx/hw+dy/hh,v=-dx/hw+dy/hh;
    if(u>=-1&&u<=1&&v>=-1&&v<=1){
      const d=Math.abs(dx)+Math.abs(dy);
      if(d<bd){bd=d;best={r,c};}
    }
  }return best;
}
function xy(e){
  const rect=cv.getBoundingClientRect(),sx=cv.width/rect.width,sy=cv.height/rect.height;
  const cl=e.touches?e.touches[0]:e;
  return{x:(cl.clientX-rect.left)*sx,y:(cl.clientY-rect.top)*sy};
}
cv.addEventListener('mousemove',e=>{const{x,y}=xy(e);hov=hit(x,y);cv.style.cursor=hov?'pointer':'default';draw();});
cv.addEventListener('mouseleave',()=>{hov=null;draw();});
cv.addEventListener('click',e=>{
  const{x,y}=xy(e),h=hit(x,y);if(!h)return;
  grid[h.r][h.c]=grid[h.r][h.c]===chosen?null:chosen;
  draw();upd();
});
cv.addEventListener('touchend',e=>{
  e.preventDefault();
  const t=e.changedTouches[0],rect=cv.getBoundingClientRect();
  const sx=cv.width/rect.width,sy=cv.height/rect.height;
  const h=hit((t.clientX-rect.left)*sx,(t.clientY-rect.top)*sy);
  if(!h)return;
  grid[h.r][h.c]=grid[h.r][h.c]===chosen?null:chosen;
  draw();upd();
},{passive:false});

function sel(k){
  chosen=k;
  Object.keys(M).forEach(id=>{
    const b=document.getElementById('btn-'+id);
    b.classList.toggle('sel',id===k);
    b.style.borderColor=id===k?M[k].color:'';
    b.style.color=id===k?M[k].color:'';
  });
}
function setBat(b){
  bat=b;
  document.getElementById('bat-AA').className='bb'+(b==='AA'?' on':'');
  document.getElementById('bat-AAA').className='bb'+(b==='AAA'?' on':'');
  upd();
}
function resetAll(){grid=Array(ROWS).fill(null).map(()=>Array(COLS).fill(null));draw();upd();}
function upd(){
  const packs=+document.getElementById('packs').value;
  const maxW=+document.getElementById('maxw').value;
  document.getElementById('pv').textContent=packs;
  document.getElementById('mv').textContent=maxW;
  const cap=BAT[bat]*packs;
  let cur=0,cnt=0;
  const cts={m120:0,m300:0,servo:0};
  grid.forEach(row=>row.forEach(m=>{if(m){cur+=M[m].amps;cnt++;cts[m]++;}}));
  const pow=+(cur*6).toFixed(2),ratio=maxW>0?pow/maxW:0;
  const pct=Math.min(ratio*100,100);
  document.getElementById('sc').textContent=cur.toFixed(2);
  document.getElementById('sp2').textContent=pow.toFixed(1);
  document.getElementById('scap').textContent=cap.toLocaleString();
  document.getElementById('scnt').textContent=cnt;
  document.getElementById('gpct').textContent=Math.round(pct)+'%';
  const gf=document.getElementById('gfill');
  gf.style.width=pct.toFixed(1)+'%';
  let gc,scls,stxt;
  if(ratio>=0.7){gc='#ef4444';scls='s-danger';stxt='⚠ 위험 — 전력 과부하!';}
  else if(ratio>=0.4){gc='#f59e0b';scls='s-warn';stxt='△ 주의 — 부하 높음';}
  else{gc='#22c55e';scls='s-safe';stxt='✓ 안전 — 정상 작동 중';}
  gf.style.background=gc;
  const pill=document.getElementById('sp');
  pill.textContent=stxt;pill.className='status-pill '+scls;
  if(cur>0){
    const mins=cap/1000/cur*60;
    document.getElementById('st').textContent=mins>=60?Math.floor(mins/60)+'h '+Math.floor(mins%60)+'m':mins.toFixed(1)+' 분';
  } else document.getElementById('st').textContent='—';
  const lids=['l0','l1','l2'],keys=['m120','m300','servo'];
  keys.forEach((k,i)=>{
    document.getElementById(lids[i]).textContent=cts[k]+'개 — '+(cts[k]*M[k].amps).toFixed(1)+'A';
  });
}
sel('m120');
window.addEventListener('resize',()=>{draw();});
setTimeout(()=>{draw();upd();},60);
</script>
</body>
</html>
""", height=620, scrolling=False)

st.markdown("---")
st.caption("⚡ 전압: 6V 기준 | 배터리 병렬 연결 | 위험 기준: 최대치의 70% 이상")
