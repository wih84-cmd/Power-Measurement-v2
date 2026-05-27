import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="프로보 에너지 모니터 Pro", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# 깔끔하고 정돈된 대시보드 스타일 지정
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; max-width: 1200px}
    footer {visibility: hidden}
    div[data-testid="stDecoration"] {background-image: linear-gradient(90deg, #6366f1, #a855f7);}
</style>
""", unsafe_allow_html=True)

st.markdown("## ⚡ 프로보 지능형 에너지 과부하 모니터")
st.caption("아래의 모터 블록을 마우스로 드래그하여 보드의 빈 슬롯에 드롭하세요. (설치 후 클릭하면 제거, 과부하 70% 이상 시 차단 고장)")

components.html("""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#0f172a;-webkit-user-select:none;user-select:none}
.app{display:grid;grid-template-columns:1fr 310px;gap:20px;background:#ffffff;border-radius:24px;padding:20px;box-shadow:0 20px 40px -15px rgba(15,23,42,0.08);border:1px solid #e2e8f0;height:670px}
.left{display:flex;flex-direction:column;background:#fdfdfd;border-radius:18px;border:1px solid #f1f5f9;padding:16px;position:relative}
.right{display:flex;flex-direction:column;gap:12px;padding:4px;overflow-y:auto;overflow-x:hidden}
.sec{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#475569;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.sec::before{content:'';display:inline-block;width:6px;height:6px;background:#6366f1;border-radius:50%}
canvas#cv{display:block;width:100%;flex:1;border-radius:14px;cursor:pointer;background:radial-gradient(circle at 50% 50%, #f8fafc 0%, #edf2f7 100%);min-height:360px;transition:transform 0.1s}
.palette-title{font-size:11px;font-weight:700;color:#64748b;margin:12px 0 4px 4px;display:flex;align-items:center;gap:4px}
.palette{display:flex;gap:10px;background:#f1f5f9;padding:10px;border-radius:14px;border:1px dashed #cbd5e1}
.mcard{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;padding:12px 8px;border-radius:10px;border:1px solid #e2e8f0;background:#fff;font-size:11px;font-weight:700;cursor:grab;color:#475569;box-shadow:0 4px 6px -1px rgba(0,0,0,0.05);transition:all .2s cubic-bezier(0.4,0,0.2,1)}
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
.sc2{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:10px;box-shadow:0 2px 4px rgba(0,0,0,0.01);transition:transform 0.2s}
.sc2:hover{transform:translateY(-2px)}
.sl{font-size:10px;color:#64748b;font-weight:600;margin-bottom:4px}
.sv{font-size:18px;font-weight:800;color:#0f172a;letter-spacing:-0.02em}
.su{font-size:10px;color:#94a3b8;font-weight:500;margin-left:2px}
.gw{display:flex;flex-direction:column;gap:5px;background:#f8fafc;padding:10px;border-radius:12px;border:1px solid #e2e8f0}
.gh{display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#334155}
.gt{height:8px;background:#e2e8f0;border-radius99px;overflow:hidden;position:relative}
.gf{height:100%;border-radius:99px;transition:width .2s ease,background .3s}
.row{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:600;color:#475569}
.row input[type=range]{flex:1;accent-color:#6366f1;cursor:pointer;height:4px}
.row b{min-width:28px;text-align:right;color:#0f172a;font-weight:800;font-size:12px}
.bat-row{display:flex;gap:6px}
.bb{flex:1;padding:8px;border:1px solid #e2e8f0;border-radius:10px;background:#fff;font-size:11px;font-weight:700;cursor:pointer;color:#475569;transition:all .15s}
.bb:hover{background:#f8fafc}
.bb.on{border-color:#6366f1;background:#f5f3ff;color:#4f46e5;box-shadow:0 0 0 1px #4f46e5}
.leg{display:flex;flex-direction:column;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:4px 10px}
.lr{display:flex;align-items:center;justify-content:space-between;font-size:11px;padding:8px 0;border-bottom:1px solid #f1f5f9}
.lr:last-child{border-bottom:none}
.ll{display:flex;align-items:center;gap:6px;color:#475569;font-weight:600}
.lv{font-weight:700;color:#0f172a}
.rbtn{width:100%;padding:10px;border:1px solid #fca5a5;border-radius:10px;background:#fff;font-size:11px;font-weight:700;cursor:pointer;color:#dc2626;transition:all .2s;margin-top:auto}
.rbtn:hover{background:#fef2f2;transform:scale(0.98)}

/* 과부하 발생 시 전체 UI 흔들림 애니메이션 효과 */
@keyframes shake {
  0%, 100% { transform: translate(0, 0); }
  20%, 60% { transform: translate(-1.5px, 1px); }
  40%, 80% { transform: translate(1.5px, -1px); }
}
.app.danger-shake{animation: shake 0.15s infinite;}
</style></head><body>
<div class="app" id="app">
  <div class="left">
    <div class="sec">로봇 메인 컴퓨터 제어 보드</div>
    <canvas id="cv" dropzone="copy"></canvas>
    <div class="palette-title">📦 드래그형 모터 소스 컴포넌트</div>
    <div class="palette">
      <div class="mcard" draggable="true" id="m120" ondragstart="ds(event)"><span class="mdot" style="background:#22c55e"></span><span>120 모터</span><span class="mamp">0.4A</span></div>
      <div class="mcard" draggable="true" id="m300" ondragstart="ds(event)"><span class="mdot" style="background:#ef4444"></span><span>300 모터</span><span class="mamp">0.8A</span></div>
      <div class="mcard" draggable="true" id="servo" ondragstart="ds(event)"><span class="mdot" style="background:#3b82f6"></span><span>서보 모터</span><span class="mamp">0.2A</span></div>
    </div>
    <div class="hint">💡 <b>드래그 앤 드롭:</b> 모터를 끌어서 보드 슬롯에 놓으세요. 배치된 블록을 <b>클릭</b>하면 제거됩니다.</div>
  </div>
  <div class="right">
    <div id="sbar" class="sbar ss">✓ 정상 작동 보증 상태</div>
    <div class="timer-wrap">
      <canvas id="tc" width="110" height="110"></canvas>
      <div style="font-size:10px;color:#64748b;font-weight:700;margin-top:4px">시스템 지속 예상 시간</div>
    </div>
    <div class="sgrid">
      <div class="sc2"><div class="sl">실시간 전류</div><div class="sv"><span id="sc">0.00</span><span class="su">A</span></div></div>
      <div class="sc2"><div class="sl">유동 전력량</div><div class="sv"><span id="sp">0.0</span><span class="su">W</span></div></div>
      <div class="sc2"><div class="sl">배터리 용량</div><div class="sv"><span id="scap">2,500</span><span class="su">mAh</span></div></div>
      <div class="sc2"><div class="sl">장착 모터 수</div><div class="sv"><span id="scnt">0</span><span class="su">개</span></div></div>
    </div>
    <div class="gw">
      <div class="gh"><span>부하율 계측</span><span id="gpct">0%</span></div>
      <div class="gt"><div class="gf" id="gfill" style="width:0%;background:#22c55e"></div></div>
    </div>
    <div class="row"><span>한계치</span><input type="range" min="5" max="50" value="15" step="1" id="maxw" oninput="upd()"><b id="mv">15</b><span>W</span></div>
    <div class="bat-row">
      <button class="bb on" id="bat-AA" onclick="setBat('AA')">AA형 셀</button>
      <button class="bb" id="bat-AAA" onclick="setBat('AAA')">AAA형 셀</button>
    </div>
    <div class="row"><span>직렬 팩</span><input type="range" min="1" max="8" value="1" step="1" id="packs" oninput="upd()"><b id="pv">1</b><span>팩</span></div>
    <div class="leg">
      <div class="lr"><span class="ll"><span class="mdot" style="background:#22c55e"></span>M120</span><span class="lv" id="l0">0개 — 0.0A</span></div>
      <div class="lr"><span class="ll"><span class="mdot" style="background:#ef4444"></span>M300</span><span class="lv" id="l1">0개 — 0.0A</span></div>
      <div class="lr"><span class="ll"><span class="mdot" style="background:#3b82f6"></span>SERVO</span><span class="lv" id="l2">0개 — 0.0A</span></div>
    </div>
    <button class="rbtn" onclick="resetAll()">↺ 모드 전체 초기화</button>
  </div>
</div>
<script>
const COLS=5,ROWS=4;
const MT={
  m120:{label:'M120',amps:0.4,top:'#a7f3d0',side:'#059669',dark:'#047857',col:'#10b981',height:24},
  m300:{label:'M300',amps:0.8,top:'#fecdd3',side:'#dc2626',dark:'#b91c1c',col:'#ef4444',height:32},
  servo:{label:'SERVO',amps:0.2,top:'#bfdbfe',side:'#2563eb',dark:'#1d4ed8',col:'#3b82f6',height:18},
};
const BAT={AA:2500,AAA:1200};
let grid=Array(ROWS).fill(null).map(()=>Array(COLS).fill(null));

// 실시간 스프링/스케일 애니메이션 보간을 위한 배열 변수
let motorScales=Array(ROWS).fill(null).map(()=>Array(COLS).fill(0));

let dragID=null,bat='AA',hov=null,broken=false;
let liveNoise=0;
let generatorGears=0;
let particles=[];

const cv=document.getElementById('cv');
const cx=cv.getContext('2d');
const tc=document.getElementById('tc');
const tx=tc.getContext('2d');
let animFrame=null;

function iso(col,row,W){
  const CW=Math.min(Math.floor(W/(COLS+1)*1.65),76);
  const CH=CW*0.54;
  const ox=W/2,oy=CH*1.6;
  return{x:ox+(col-row)*(CW/2),y:oy+(col+row)*(CH/2),cw:CW,ch:CH};
}

// 고성능 2D Canvas 렌더링 내에 실시간 애니메이션 가미 (회전축, 고장 파괴선)
function drawMotorShape(cx2,x,y,cw,ch,m,isHov,scale){
  const hw=cw/2*scale,hh=ch/2*scale,bh=m.height*scale;
  if(scale<=0.01)return;
  cx2.save();
  cx2.translate(x,y);
  
  // 마우스 호버(드래그 오버 포함) 시 실시간 살짝 위로 들어올려지는 붕 뜬 시각 효과 유도
  if(isHov && !broken) cx2.translate(0, -5);

  cx2.beginPath();
  cx2.moveTo(0,-hh);cx2.lineTo(hw,0);cx2.lineTo(0,hh);cx2.lineTo(-hw,0);
  cx2.closePath();cx2.fillStyle=m.top;cx2.fill();
  if(isHov){cx2.fillStyle='rgba(255,255,255,0.25)';cx2.fill();}
  
  cx2.beginPath();
  cx2.moveTo(-hw,0);cx2.lineTo(0,hh);cx2.lineTo(0,hh+bh);cx2.lineTo(-hw,bh);
  cx2.closePath();cx2.fillStyle=m.dark;cx2.fill();
  
  cx2.beginPath();
  cx2.moveTo(hw,0);cx2.lineTo(0,hh);cx2.lineTo(0,hh+bh);cx2.lineTo(hw,bh);
  cx2.closePath();cx2.fillStyle=m.side;cx2.fill();
  
  // 모터 중앙 회전 기믹 축 샤프트부 생성
  const cr=hw*0.35;
  cx2.beginPath();cx2.arc(0,0,cr,0,Math.PI*2);
  cx2.fillStyle='rgba(255,255,255,0.4)';cx2.fill();
  
  cx2.save();
  if(!broken && getRawPow()>0){
    // 소모 전력 수치 비례 가변 실시간 틱 회전 로직
    cx2.rotate((Date.now()/120)*(m.amps*2.5));
  }
  cx2.beginPath();cx2.rect(-2,-2,4,4);
  cx2.fillStyle='#1e293b';cx2.fill();
  cx2.restore();

  cx2.fillStyle='rgba(15,23,42,0.85)';
  cx2.font='bold '+Math.round(cw*0.13)+'px system-ui';
  cx2.textAlign='center';cx2.textBaseline='middle';
  cx2.fillText(m.label,0,-hh*0.1);
  
  // 고장 상태 크랙 드로잉
  if(broken){
    cx2.fillStyle='rgba(220,38,38,0.15)';cx2.fill();
    cx2.strokeStyle='#ef4444';cx2.lineWidth=2;
    cx2.beginPath();cx2.moveTo(-hw*0.4,-hh*0.4);cx2.lineTo(hw*0.4,hh*0.4);cx2.stroke();
    cx2.beginPath();cx2.moveTo(hw*0.4,-hh*0.4);cx2.lineTo(-hw*0.4,hh*0.4);cx2.stroke();
  }
  cx2.restore();
}

function getRawPow(){
  let c=0;grid.forEach(r=>r.forEach(m=>{if(m)c+=MT[m].amps;}));
  return c*6;
}

function getPow(){
  let base=getRawPow();
  if(base===0)return 0;
  return +(base + liveNoise).toFixed(2);
}

function getMaxW(){return+document.getElementById('maxw').value||15;}

// 하단 발전기 애니메이션 (연기 파티클 및 과부하 스파크 연출)
function drawComplexMachine(cx2,W,H){
  const mx=W*0.5,my=H-65;
  const isOperating=!broken && getRawPow()>0;
  
  if(isOperating) {
    generatorGears += (getRawPow()*0.04);
    if(Math.random()<0.18) {
      particles.push({x:mx-25+Math.random()*10,y:my-25,vx:-0.2+Math.random()*0.4,vy:-1-Math.random(),alpha:1,size:3+Math.random()*4,type:'smoke'});
    }
  }
  if(broken && Math.random()<0.4) {
    particles.push({x:mx-40+Math.random()*80,y:my-30+Math.random()*40,vx:-2+Math.random()*4,vy:-2-Math.random()*3,alpha:1,size:1.5+Math.random()*2,type:'spark'});
  }

  particles.forEach((p,idx)=>{
    p.x+=p.vx;p.y+=p.vy;p.alpha-=0.02;
    if(p.type==='smoke'){
      cx2.fillStyle=`rgba(148,163,184,${p.alpha*0.4})`;
      cx2.beginPath();cx2.arc(p.x,p.y,p.size,0,Math.PI*2);cx2.fill();
    }else{
      cx2.fillStyle=`rgba(251,191,36,${p.alpha})`;
      cx2.beginPath();cx2.arc(p.x,p.y,p.size,0,Math.PI*2);cx2.fill();
    }
    if(p.alpha<=0)particles.splice(idx,1);
  });

  cx2.save();
  cx2.shadowBlur=12;
  cx2.shadowColor=broken?'rgba(239,68,68,0.2)':'rgba(148,163,184,0.15)';
  
  let grd=cx2.createLinearGradient(mx-50,my,mx+50,my);
  grd.addColorStop(0,'#334155');grd.addColorStop(0.5,'#475569');grd.addColorStop(1,'#1e293b');
  cx2.fillStyle=grd;
  cx2.beginPath();cx2.roundRect(mx-45,my-15,90,40,8);cx2.fill();
  cx2.restore();

  cx2.save();
  cx2.translate(mx-22,my+5);
  if(isOperating)cx2.rotate(generatorGears);
  cx2.strokeStyle='#94a3b8';cx2.lineWidth=2;
  cx2.beginPath();cx2.arc(0,0,10,0,Math.PI*2);cx2.stroke();
  for(let i=0;i<6;i++){
    cx2.rotate(Math.PI/3);
    cx2.fillStyle='#64748b';cx2.fillRect(-2,-12,4,4);
  }
  cx2.restore();

  cx2.fillStyle='#1e293b';cx2.beginPath();cx2.roundRect(mx+10,my-3,28,16,3);cx2.fill();
  cx2.fillStyle=broken?'#ef4444':isOperating?'#10b981':'#64748b';
  cx2.beginPath();cx2.arc(mx+24,my+5,4,0,Math.PI*2);cx2.fill();

  cx2.fillStyle='#64748b';
  cx2.fillRect(mx-30,my-28,12,14);

  cx2.fillStyle='#475569';cx2.font='bold 11px system-ui';cx2.textAlign='center';
  cx2.fillText(broken?'SYSTEM FAIL (과부하)':isOperating?'GENERATOR RUNNING':'STANDBY',mx,my+42);
}

function drawBoard(){
  const W=cv.offsetWidth*devicePixelRatio||430;
  const H=cv.offsetHeight*devicePixelRatio||370;
  if(cv.width!==W||cv.height!==H){cv.width=W;cv.height=H;}
  
  cx.clearRect(0,0,W,H);
  
  // 바닥 격자판 타일 빌드
  for(let r=ROWS-1;r>=0;r--){
    for(let c=COLS-1;c>=0;c--){
      const p=iso(c,r,W),hw=p.cw/2,hh=p.ch/2;
      cx.beginPath();
      cx.moveTo(p.x,p.y-hh);cx.lineTo(p.x+hw,p.y);cx.lineTo(p.x,p.y+hh);cx.lineTo(p.x-hw,p.y);
      cx.closePath();
      cx.fillStyle='#ffffff';cx.fill();
      cx.strokeStyle='rgba(99,102,241,0.08)';cx.lineWidth=1;cx.stroke();
      
      // 드래그 또는 마우스 호버 타겟 시 하이라이트 투명 레이어
      if(hov&&hov.r===r&&hov.c===c&&!grid[r][c]){
        cx.fillStyle='rgba(99,102,241,0.15)';cx.fill();
      }
      
      cx.fillStyle='#94a3b8';cx.font='600 '+Math.round(p.cw*0.14)+'px system-ui';
      cx.textAlign='center';cx.textBaseline='middle';
      cx.fillText(r*COLS+c+1,p.x,p.y);
    }
  }
  
  // 타일 위 모터 개체 유동 렌더링
  for(let r=ROWS-1;r>=0;r--){
    for(let c=COLS-1;c>=0;c--){
      const m=grid[r][c];
      let targetScale=m?1:0;
      // 스프링 스무딩 배율 애니메이션 계산
      motorScales[r][c]+=(targetScale-motorScales[r][c])*0.22; 
      
      if(motorScales[r][c]>0.001){
        const p=iso(c,r,W);
        drawMotorShape(cx,p.x,p.y,p.cw,p.ch,MT[m||dragID],hov&&hov.r===r&&hov.c===c,motorScales[r][c]);
      }
    }
  }
  drawComplexMachine(cx,W,H);
}

function hit(mx,my){
  const W=cv.width;let best=null,bd=999;
  for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){
    const p=iso(c,r,W),hw=p.cw/2,hh=p.ch/2;
    const dx=mx-p.x,dy=my-p.y,u=dx/hw+dy/hh,v=-dx/hw+dy/hh;
    if(u>=-1&&u<=1&&v>=-1&&v<=1){const d=Math.abs(dx)+Math.abs(dy);if(d<bd){bd=d;best={r,c};}}
  }return best;
}

function xy(e){
  const rect=cv.getBoundingClientRect(),sx=cv.width/rect.width,sy=cv.height/rect.height;
  const cl=e.touches?e.touches[0]:e;
  return{x:(cl.clientX-rect.left)*sx,y:(cl.clientY-rect.top)*sy};
}

// 오리지널 드래그 앤 드롭 트리거 자바스크립트 연동 이벤트
function ds(e){ dragID = e.target.id; }
cv.addEventListener('dragover',e=>{e.preventDefault();const p=xy(e);hov=hit(p.x,p.y);});
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

function drawTimer(mins,maxM){
  const W=110,cx2=W/2,cy=W/2,R=42,lw=7;
  tx.clearRect(0,0,W,W);
  tx.beginPath();tx.arc(cx2,cy,R,0,Math.PI*2);
  tx.strokeStyle='#f1f5f9';tx.lineWidth=lw;tx.stroke();
  if(mins!==null&&maxM>0){
    const frac=Math.min(mins/maxM,1);
    const col=frac>0.6?'#10b981':frac>0.25?'#f59e0b':'#ef4444';
    tx.beginPath();tx.arc(cx2,cy,R,-Math.PI/2,-Math.PI/2+frac*Math.PI*2);
    tx.strokeStyle=col;tx.lineWidth=lw;tx.lineCap='round';tx.stroke();
  }
  tx.textAlign='center';tx.textBaseline='middle';
  if(mins===null){tx.fillStyle='#94a3b8';tx.font='bold 14px system-ui';tx.fillText('대기중',cx2,cy);}
  else if(broken){tx.fillStyle='#ef4444';tx.font='bold 14px system-ui';tx.fillText('SYSTEM DOWN',cx2,cy);}
  else if(mins>=60){
    tx.fillStyle='#0f172a';tx.font='bold 13px system-ui';tx.fillText(Math.floor(mins/60)+'시간',cx2,cy-6);
    tx.font='600 10px system-ui';tx.fillStyle='#64748b';tx.fillText(Math.floor(mins%60)+'분',cx2,cy+8);
  } else {
    tx.fillStyle='#0f172a';tx.font='800 17px system-ui';tx.fillText(mins.toFixed(1),cx2,cy-4);
    tx.font='600 10px system-ui';tx.fillStyle='#64748b';tx.fillText('분 가동',cx2,cy+10);
  }
}

function startAnim(){if(animFrame)return;function loop(){
  // 가동 상태일 때 미세 저항 및 전력 오차 노이즈 반영 시뮬레이션 구현
  if(getRawPow()>0 && !broken) {
    liveNoise = Math.sin(Date.now()/120) * 0.18 + (Math.random()-0.5)*0.08;
  } else {
    liveNoise = 0;
  }
  
  const pNow = getPow();
  if(getRawPow()>0 && !broken){
    document.getElementById('sp').textContent=pNow.toFixed(2);
    document.getElementById('sc').textContent=(pNow/6).toFixed(2);
  }

  drawBoard();
  animFrame=requestAnimationFrame(loop);
}loop();}

function upd(){
  const packs=+document.getElementById('packs').value,maxW=+document.getElementById('maxw').value;
  document.getElementById('pv').textContent=packs;document.getElementById('mv').textContent=maxW;
  const cap=BAT[bat]*packs;let cur=0,cnt=0;const cts={m120:0,m300:0,servo:0};
  grid.forEach(row=>row.forEach(m=>{if(m){cur+=MT[m].amps;cnt++;cts[m]++;}}));
  
  const pow=getRawPow(),ratio=maxW>0?pow/maxW:0,pct=Math.min(ratio*100,100);
  broken=ratio>=0.7;
  
  // 과부하 걸리면 전체 대시보드 구조에 떨림 CSS 클래스 연동
  document.getElementById('app').classList.toggle('danger-shake', broken);

  document.getElementById('sc').textContent=cur.toFixed(2);
  document.getElementById('sp').textContent=pow.toFixed(1);
  document.getElementById('scap').textContent=cap.toLocaleString();
  document.getElementById('scnt').textContent=cnt;
  document.getElementById('gpct').textContent=Math.round(pct)+'%';
  const gf=document.getElementById('gfill');gf.style.width=pct.toFixed(1)+'%';
  let gc,scls,stxt;
  if(ratio>=0.7){gc='#ef4444';scls='sd';stxt='❌ 과부하 차단 — 시스템 긴급 고장';}
  else if(ratio>=0.4){gc='#f59e0b';scls='sw';stxt='⚠ 경고 — 임계 부하 영역 진입';}
  else{gc='#10b981';scls='ss';stxt='✓ 안전 — 실시간 전력 분배 안정화';}
  gf.style.background=gc;
  const sb=document.getElementById('sbar');sb.textContent=stxt;sb.className='sbar '+scls;
  const mins=cur>0?cap/1000/cur*60:null;
  drawTimer(mins,60);
  ['m120','m300','servo'].forEach((k,i)=>{document.getElementById('l'+i).textContent=cts[k]+'개 — '+(cts[k]*MT[k].amps).toFixed(1)+'A';});
  
  startAnim();
}

new ResizeObserver(()=>{drawBoard();}).observe(cv);
setTimeout(()=>{drawBoard();upd();},100);
</script></body></html>""", height=710, scrolling=False)

st.markdown("---")
st.caption("⚙️ 정밀 제어 시스템 | 가동 중 실시간 미세 저항 및 전력 오차 시뮬레이션 활성화 완료")
