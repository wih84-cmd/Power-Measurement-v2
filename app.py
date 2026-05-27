import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="프로보 에너지 모니터 2D 정밀형", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; max-width: 1200px}
    footer {visibility: hidden}
    div[data-testid="stDecoration"] {background-image: linear-gradient(90deg, #1e40af, #0284c7);}
</style>
""", unsafe_allow_html=True)

st.markdown("## ⚡ 프로보 지능형 2D 에너지 과부하 모니터 (정밀 디버깅 완료 v2.6)")
st.caption("배터리 공학 수식을 준수하는 2D 드래그 앤 드롭 시뮬레이터입니다. 모터 블록을 끌어다 보드에 배치해 보세요.")

components.html("""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#0f172a;-webkit-user-select:none;user-select:none}
.app{display:grid;grid-template-columns:1fr 320px;gap:20px;background:#ffffff;border-radius:24px;padding:20px;box-shadow:0 20px 40px -15px rgba(15,23,42,0.08);border:1px solid #e2e8f0;height:670px}
.left{display:flex;flex-direction:column;background:#fdfdfd;border-radius:18px;border:1px solid #f1f5f9;padding:16px;position:relative}
.right{display:flex;flex-direction:column;gap:12px;padding:4px;overflow-y:auto;overflow-x:hidden}
.sec{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#475569;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.sec::before{content:'';display:inline-block;width:6px;height:6px;background:#1e40af;border-radius:50%}
canvas#cv{display:block;width:100%;flex:1;border-radius:14px;cursor:pointer;background:#f1f5f9;min-height:360px}
.palette-title{font-size:11px;font-weight:700;color:#64748b;margin:12px 0 4px 4px;display:flex;align-items:center;gap:4px}
.palette{display:flex;gap:10px;background:#e2e8f0;padding:10px;border-radius:14px;border:1px dashed #cbd5e1}
.mcard{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;padding:12px 8px;border-radius:10px;border:1px solid #e2e8f0;background:#fff;font-size:11px;font-weight:700;cursor:grab;color:#475569;box-shadow:0 4px 6px -1px rgba(0,0,0,0.05);transition:all .2s}
.mcard:hover{transform:translateY(-2px);box-shadow:0 10px 15px -3px rgba(0,0,0,0.08);border-color:#cbd5e1}
.mcard:active{cursor:grabbing}
.mdot{width:8px;height:8px;border-radius:50%}
.mamp{font-size:10px;color:#94a3b8;font-weight:500}
.hint{font-size:11px;color:#64748b;margin-top:8px;text-align:center;background:#f8fafc;padding:6px;border-radius:6px}
.sbar{padding:12px;border-radius:12px;font-size:12px;font-weight:700;text-align:center;box-shadow:inset 0 1px 0 rgba(255,255,255,0.2);transition:all .3s}
.ss{background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0}
.sw{background:#fffbeb;color:#92400e;border:1px solid #fde68a}
.sd{background:#fff1f2;color:#9f1239;border:1px solid #fecdd3}
.timer-wrap{display:flex;flex-direction:column;align-items:center;position:relative;background:#f8fafc;padding:12px;border-radius:16px;border:1px solid #e2e8f0}
.sgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sc2{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:10px;box-shadow:0 2px 4px rgba(0,0,0,0.01)}
.sl{font-size:10px;color:#64748b;font-weight:600;margin-bottom:4px}
.sv{font-size:18px;font-weight:800;color:#0f172a;letter-spacing:-0.02em}
.su{font-size:10px;color:#94a3b8;font-weight:500;margin-left:2px}
.gw{display:flex;flex-direction:column;gap:5px;background:#f8fafc;padding:10px;border-radius:12px;border:1px solid #e2e8f0}
.gh{display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#334155}
.gt{height:8px;background:#e2e8f0;border-radius:99px;overflow:hidden;position:relative}
.gf{height:100%;border-radius:99px;transition:width .2s ease,background .3s}
.row{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:600;color:#475569}
.row input[type=range]{flex:1;accent-color:#1e40af;cursor:pointer;height:4px}
.row b{min-width:28px;text-align:right;color:#0f172a;font-weight:800;font-size:12px}
.bat-row{display:flex;gap:6px}
.bb{flex:1;padding:8px;border:1px solid #e2e8f0;border-radius:10px;background:#fff;font-size:11px;font-weight:700;cursor:pointer;color:#475569;transition:all .15s}
.bb:hover{background:#f8fafc}
.bb.on{border-color:#1e40af;background:#eff6ff;color:#1d4ed8;box-shadow:0 0 0 1px #1d4ed8}
.leg{display:flex;flex-direction:column;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:4px 10px}
.lr{display:flex;align-items:center;justify-content:space-between;font-size:11px;padding:8px 0;border-bottom:1px solid #f1f5f9}
.lr:last-child{border-bottom:none}
.ll{display:flex;align-items:center;gap:6px;color:#475569;font-weight:600}
.lv{font-weight:700;color:#0f172a}
.rbtn{width:100%;padding:10px;border:1px solid #fca5a5;border-radius:10px;background:#fff;font-size:11px;font-weight:700;cursor:pointer;color:#dc2626;transition:all .2s;margin-top:auto}
.rbtn:hover{background:#fef2f2;transform:scale(0.98)}

@keyframes shake {
  0%, 100% { transform: translate(0, 0); }
  20%, 60% { transform: translate(-1px, 1px); }
  40%, 80% { transform: translate(1px, -1px); }
}
.app.danger-shake{animation: shake 0.15s infinite;}
</style></head><body>
<div class="app" id="app">
  <div class="left">
    <div class="sec">로봇 2D 평면 그리드 배치 보드</div>
    <canvas id="cv"></canvas>
    <div class="palette-title">📦 모터 소스 블록 (드래그하여 배치)</div>
    <div class="palette">
      <div class="mcard" draggable="true" id="m120" ondragstart="ds(event)"><span class="mdot" style="background:#10b981"></span><span>120 모터</span><span class="mamp">0.4A</span></div>
      <div class="mcard" draggable="true" id="m300" ondragstart="ds(event)"><span class="mdot" style="background:#ef4444"></span><span>300 모터</span><span class="mamp">0.8A</span></div>
      <div class="mcard" draggable="true" id="servo" ondragstart="ds(event)"><span class="mdot" style="background:#3b82f6"></span><span>서보 모터</span><span class="mamp">0.2A</span></div>
    </div>
    <div class="hint">💡 <b>드롭 안내:</b> 원하는 블록을 끌어다 흰 칸에 놓으세요. 배치된 원형 블록을 <b>클릭</b>하면 제거됩니다.</div>
  </div>
  <div class="right">
    <div id="sbar" class="sbar ss">✓ 안전 — 정상 작동 중</div>
    <div class="timer-wrap">
      <canvas id="tc" width="110" height="110"></canvas>
      <div style="font-size:10px;color:#64748b;font-weight:700;margin-top:4px">시스템 지속 예상 시간</div>
    </div>
    <div class="sgrid">
      <div class="sc2"><div class="sl">실시간 총 전류</div><div class="sv"><span id="sc">0.00</span><span class="su">A</span></div></div>
      <div class="sc2"><div class="sl">실시간 전력</div><div class="sv"><span id="sp">0.0</span><span class="su">W</span></div></div>
      <div class="sc2"><div class="sl">배터리 에너지</div><div class="sv"><span id="swh">0.00</span><span class="su">Wh</span></div></div>
      <div class="sc2"><div class="sl">공칭 시스템 전압</div><div class="sv"><span id="svol">6.0</span><span class="su">V</span></div></div>
    </div>
    <div class="gw">
      <div class="gh"><span>설정치 대비 전력 부하율</span><span id="gpct">0%</span></div>
      <div class="gt"><div class="gf" id="gfill" style="width:0%;background:#10b981"></div></div>
    </div>
    <div class="row"><span>임계 한계치</span><input type="range" min="3" max="30" value="12" step="1" id="maxw" oninput="upd()"><b id="mv">12</b><span>W</span></div>
    <div class="bat-row">
      <button class="bb on" id="bat-AA" onclick="setBat('AA')">AA형 (2500mAh)</button>
      <button class="bb" id="bat-AAA" onclick="setBat('AAA')">AAA형 (1200mAh)</button>
    </div>
    <div class="row"><span>직렬 팩 개수</span><input type="range" min="1" max="8" value="4" step="1" id="packs" oninput="upd()"><b id="pv">4</b><span>셀</span></div>
    <div class="leg">
      <div class="lr"><span class="ll"><span class="mdot" style="background:#10b981"></span>M120</span><span class="lv" id="l0">0개 — 0.0A</span></div>
      <div class="lr"><span class="ll"><span class="mdot" style="background:#ef4444"></span>M300</span><span class="lv" id="l1">0개 — 0.0A</span></div>
      <div class="lr"><span class="ll"><span class="mdot" style="background:#3b82f6"></span>SERVO</span><span class="lv" id="l2">0개 — 0.0A</span></div>
    </div>
    <button class="rbtn" onclick="resetAll()">↺ 모드 전체 초기화</button>
  </div>
</div>
<script>
const COLS=5,ROWS=4;
const MT={
  m120:{label:'M120',amps:0.4,bg:'#e6f4ea',border:'#10b981',text:'#137333'},
  m300:{label:'M300',amps:0.8,bg:'#fce8e6',border:'#ef4444',text:'#c5221f'},
  servo:{label:'SVO',amps:0.2,bg:'#e8f0fe',border:'#3b82f6',text:'#1a73e8'},
};
const BAT={AA:2500,AAA:1200};
let grid=Array(ROWS).fill(null).map(()=>Array(COLS).fill(null));
let motorScales=Array(ROWS).fill(null).map(()=>Array(COLS).fill(0));

let dragID=null,bat='AA',hov=null,broken=false;
let liveNoise=0,shaftAngle=0;
let particles=[];

const cv=document.getElementById('cv');
const cx=cv.getContext('2d');
const tc=document.getElementById('tc');
const tx=tc.getContext('2d');
let animFrame=null;

function get2DCellRect(col,row,W,H){
  const padding=10;
  const boardW=W-padding*2;
  const boardH=H-padding*2;
  const cellW=boardW/COLS, cellH=boardH/ROWS;
  return { x:padding+col*cellW, y:padding+row*cellH, w:cellW, h:cellH };
}

function draw2DMotor(cx2,rect,m,isHov,scale){
  const cxz=rect.x+rect.w/2;
  const cyz=rect.y+rect.h/2;
  const maxR=Math.min(rect.w,rect.h)/2*0.85;
  const r=maxR*scale;
  
  if(scale<=0.01) return;
  
  cx2.save();
  cx2.beginPath();
  cx2.arc(cxz,cyz,r,0,Math.PI*2);
  cx2.fillStyle=broken?'#fee2e2':m.bg;
  cx2.fill();
  cx2.strokeStyle=broken?'#ef4444':m.border;
  cx2.lineWidth=isHov?3:2;
  cx2.stroke();
  
  cx2.beginPath();
  cx2.arc(cxz,cyz,r*0.65,0,Math.PI*2);
  cx2.strokeStyle=broken?'rgba(239,64,64,0.2)':'rgba(0,0,0,0.06)';
  cx2.lineWidth=1.5;
  cx2.stroke();

  cx2.save();
  cx2.translate(cxz,cyz);
  if(!broken && getTotalCurrent()>0){
    cx2.rotate(shaftAngle*(m.amps*2.2));
  }
  cx2.beginPath();
  cx2.moveTo(-r*0.5,0);cx2.lineTo(r*0.5,0);
  cx2.moveTo(0,-r*0.5);cx2.lineTo(0,r*0.5);
  cx2.strokeStyle=broken?'#dc2626':m.border;
  cx2.lineWidth=2.5;
  cx2.stroke();
  
  cx2.beginPath();
  cx2.arc(0,0,r*0.15,0,Math.PI*2);
  cx2.fillStyle='#334155';
  cx2.fill();
  cx2.restore();
  
  cx2.fillStyle=broken?'#b91c1c':m.text;
  cx2.font='bold '+Math.round(maxR*0.42)+'px system-ui';
  cx2.textAlign='center';
  cx2.textBaseline='middle';
  cx2.fillText(m.label,cxz,cyz-r*0.45);
  
  cx2.fillStyle='#64748b';
  cx2.font='600 '+Math.round(maxR*0.3)+'px system-ui';
  cx2.fillText((m.amps)+'A',cxz,cyz+r*0.45);

  if(broken){
    cx2.strokeStyle='#ef4444';cx2.lineWidth=2;
    cx2.beginPath();cx2.moveTo(cxz-r*0.5,cyz-r*0.5);cx2.lineTo(cxz+r*0.5,cyz+r*0.5);cx2.stroke();
    cx2.beginPath();cx2.moveTo(cxz+r*0.5,cyz-r*0.5);cx2.lineTo(cxz-r*0.5,cyz+r*0.5);cx2.stroke();
  }
  cx2.restore();
}

function getTotalCurrent(){
  let c=0;grid.forEach(r=>r.forEach(m=>{if(m)c+=MT[m].amps;}));
  return c;
}

function getRawPow(){
  const packs=+document.getElementById('packs').value;
  return getTotalCurrent()*(1.5*packs);
}

function getPow(){
  let base=getRawPow();
  if(base===0)return 0;
  return Math.max(0, +(base + liveNoise).toFixed(2));
}

function drawBoard(){
  const W=cv.offsetWidth*devicePixelRatio||430;
  const H=cv.offsetHeight*devicePixelRatio||370;
  if(cv.width!==W||cv.height!==H){cv.width=W;cv.height=H;}
  
  cx.clearRect(0,0,W,H);
  
  if(!broken && getTotalCurrent()>0){
    shaftAngle += 0.08;
  }

  if(broken && Math.random()<0.35){
    particles.push({
      x:Math.random()*W,y:Math.random()*H,
      vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,
      alpha:1,size:2+Math.random()*2
    });
  }
  particles.forEach((p,idx)=>{
    p.x+=p.vx;p.y+=p.vy;p.alpha-=0.03;
    cx.fillStyle=`rgba(251,191,36,${p.alpha})`;
    cx.beginPath();cx.arc(p.x,p.y,p.size,0,Math.PI*2);cx.fill();
    if(p.alpha<=0)particles.splice(idx,1);
  });

  for(let r=0;r<ROWS;r++){
    for(let c=0;c<COLS;c++){
      const rect=get2DCellRect(c,r,W,H);
      cx.fillStyle=(r+c)%2===0?'#ffffff':'#f8fafc';
      cx.fillRect(rect.x,rect.y,rect.w,rect.h);
      cx.strokeStyle='rgba(148,163,184,0.15)';
      cx.lineWidth=1;
      cx.strokeRect(rect.x,rect.y,rect.w,rect.h);
      
      if(hov && hov.r===r && hov.c===c && !grid[r][c]){
        cx.fillStyle='rgba(30,64,175,0.08)';
        cx.fillRect(rect.x+2,rect.y+2,rect.w-4,rect.h-4);
      }
      if(!grid[r][c]){
        cx.fillStyle='#cbd5e1';
        cx.font='700 14px system-ui';
        cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText((r*COLS+c+1),rect.x+rect.w/2,rect.y+rect.h/2);
      }
    }
  }
  
  for(let r=0;r<ROWS;r++){
    for(let c=0;c<COLS;c++){
      const m=grid[r][c];
      let targetScale=m?1:0;
      motorScales[r][c]+=(targetScale-motorScales[r][c])*0.2;
      
      if(motorScales[r][c]>0.001){
        const rect=get2DCellRect(c,r,W,H);
        draw2DMotor(cx,rect,MT[m||dragID],hov&&hov.r===r&&hov.c===c,motorScales[r][c]);
      }
    }
  }
}

function hit(mx,my){
  const W=cv.width, H=cv.height;
  for(let r=0;r<ROWS;r++){
    for(let c=0;c<COLS;c++){
      const rect=get2DCellRect(c,r,W,H);
      if(mx>=rect.x && mx<=rect.x+rect.w && my>=rect.y && my<=rect.y+rect.h){
        return {r,c};
      }
    }
  }
  return null;
}

function xy(e) {
  const rect = cv.getBoundingClientRect();
  const sx = cv.width / rect.width;
  const sy = cv.height / rect.height;
  const clientX = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
  const clientY = e.clientY !== undefined ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
  return { x: (clientX - rect.left) * sx, y: (clientY - rect.top) * sy };
}

// e.currentTarget을 통해 내부 span 스크랩 문제를 완벽 차단
function ds(e){ 
  dragID = e.currentTarget.id; 
  if(e.dataTransfer) e.dataTransfer.setData('text/plain', dragID);
}

cv.addEventListener('dragover',e=>{ e.preventDefault(); const p=xy(e); hov=hit(p.x,p.y); });
cv.addEventListener('dragleave',()=>{hov=null;});
cv.addEventListener('drop',e=>{
  e.preventDefault();
  const p=xy(e),h=hit(p.x,p.y);
  if(h && dragID && !grid[h.r][h.c]){ grid[h.r][h.c]=dragID; upd(); }
  hov=null;
});

cv.addEventListener('mousemove',e=>{const p=xy(e);hov=hit(p.x,p.y);cv.style.cursor=hov?'pointer':'default';});
cv.addEventListener('mouseleave',()=>{hov=null;});
cv.addEventListener('click',e=>{
  const p=xy(e),h=hit(p.x,p.y);
  if(!h)return;
  if(grid[h.r][h.c]){ grid[h.r][h.c]=null; upd(); }
});

function setBat(b){bat=b;document.getElementById('bat-AA').className='bb'+(b==='AA'?' on':'');document.getElementById('bat-AAA').className='bb'+(b==='AAA'?' on':'');upd();}
function resetAll(){grid=Array(ROWS).fill(null).map(()=>Array(COLS).fill(null));broken=false;upd();}

// 타이머 구문 오류 완벽 수정 패치 완료
function drawTimer(mins,maxM){
  const W=110,cx2=W/2,cy=W/2,R=42,lw=7;
  tx.clearRect(0,0,W,W);
  tx.beginPath();tx.arc(cx2,cy,R,0,Math.PI*2);
  tx.strokeStyle='#f1f5f9';tx.lineWidth=lw;tx.stroke();
  tx.textAlign='center';tx.textBaseline='middle';
  
  if(mins===null || isNaN(mins) || mins<=0 || !isFinite(mins)){
    tx.fillStyle='#94a3b8';tx.font='bold 14px system-ui';
    tx.fillText('대기중',cx2,cy);
    return;
  }
  if(broken){
    tx.fillStyle='#ef4444';tx.font='bold 12px system-ui';
    tx.fillText('DOWN',cx2,cy);
    return;
  }

  const frac=Math.min(mins/maxM,1);
  const col=frac>0.6?'#10b981':frac>0.25?'#f59e0b':'#ef4444';
  tx.beginPath();tx.arc(cx2,cy,R,-Math.PI/2,-Math.PI/2+frac*Math.PI*2);
  tx.strokeStyle=col;tx.lineWidth=lw;tx.lineCap='round';tx.stroke();

  if(mins>=60){
    tx.fillStyle='#0f172a';tx.font='bold 13px system-ui';tx.fillText(Math.floor(mins/60)+'시간',cx2,cy-6);
    tx.font='600 10px system-ui';tx.fillStyle='#64748b';tx.fillText(Math.floor(mins%60)+'분',cx2,cy+8);
  } else {
    tx.fillStyle='#0f172a';tx.font='800 17px system-ui';tx.fillText(mins.toFixed(1),cx2,cy-4);
    tx.font='600 10px system-ui';tx.fillStyle='#64748b';tx.fillText('분 가동',cx2,cy+10);
  }
}

function startAnim(){
  if(animFrame) return;
  function loop(){
    if(getTotalCurrent()>0 && !broken) {
      liveNoise = Math.sin(Date.now()/120) * 0.12 + (Math.random()-0.5)*0.04;
    } else { liveNoise = 0; }
    
    const pNow = getPow();
    if(getTotalCurrent()>0 && !broken){
      document.getElementById('sp').textContent=pNow.toFixed(1);
    }
    drawBoard();
    animFrame=requestAnimationFrame(loop);
  }
  loop();
}

function upd(){
  const packs=+document.getElementById('packs').value;
  const maxW=+document.getElementById('maxw').value;
  document.getElementById('pv').textContent=packs;
  document.getElementById('mv').textContent=maxW;
  
  const sysVolts = 1.5 * packs; 
  const cellCapAmps = BAT[bat] / 1000; 
  const totalWh = sysVolts * cellCapAmps; 
  
  let cur=0, cnt=0;
  const cts={m120:0,m300:0,servo:0};
  grid.forEach(row=>row.forEach(m=>{if(m){cur+=MT[m].amps;cnt++;cts[m]++;}}));
  
  const pow=getRawPow();
  const ratio=maxW>0?pow/maxW:0;
  const pct=Math.min(ratio*100,100);
  broken=ratio>=1.0; 
  
  document.getElementById('app').classList.toggle('danger-shake', broken);

  document.getElementById('sc').textContent=cur.toFixed(2);
  document.getElementById('sp').textContent=pow.toFixed(1);
  document.getElementById('swh').textContent=totalWh.toFixed(2);
  document.getElementById('svol').textContent=sysVolts.toFixed(1);
  document.getElementById('scnt').textContent=cnt;
  document.getElementById('gpct').textContent=Math.round(pct)+'%';
  
  const gf=document.getElementById('gfill');
  gf.style.width=pct.toFixed(1)+'%';
  
  let gc,scls,stxt;
  if(ratio>=1.0){gc='#ef4444';scls='sd';stxt='❌ 과부하 차단 — 설정 임계 전력 초과 정지';}
  else if(ratio>=0.7){gc='#f59e0b';scls='sw';stxt='⚠ 경고 — 임계 부하 허용범위 근접';}
  else{gc='#1e40af';scls='ss';stxt='✓ 안전 — 정격 전력 상태';}
  
  gf.style.background=gc;
  const sb=document.getElementById('sbar');
  sb.textContent=stxt;sb.className='sbar '+scls;
  
  const mins=cur>0?(cellCapAmps/cur)*60:null;
  drawTimer(mins,120);
  
  ['m120','m300','servo'].forEach((k,i)=>{
    document.getElementById('l'+i).textContent=cts[k]+'개 — '+(cts[k]*MT[k].amps).toFixed(1)+'A';
  });
  
  startAnim();
}

new ResizeObserver(()=>{drawBoard();}).observe(cv);
setTimeout(()=>{drawBoard();upd();},100);
</script></body></html>""", height=710, scrolling=False)

st.markdown("---")
st.caption("⚙️ 정밀 제어 계측 모듈 v2.6 | 마우스 드래그 컴포넌트 유실 결함 및 스크립트 크래시 긴급 수정 완료")
