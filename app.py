import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="프로보 에너지 모니터",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 전역 상수 ──────────────────────────────────────────────
BATTERY_SPECS = {
    "AA": {"capacity_mah": 2500, "label": "AA (오래감)", "color": "#3b82f6"},
    "AAA": {"capacity_mah": 1200, "label": "AAA (가벼움)", "color": "#8b5cf6"},
}
CELLS_PER_PACK = 4
ROBOT_VOLTAGE = 6.0

MOTOR_SPECS = {
    "m120": {"current_a": 0.4, "label": "120 모터", "color": "#22c55e", "icon": "⚡"},
    "m300": {"current_a": 0.8, "label": "300 모터", "color": "#ef4444", "icon": "🔥"},
    "servo": {"current_a": 0.2, "label": "서보 모터", "color": "#3b82f6", "icon": "🎯"},
}

SLOT_COUNT = 8  # 로봇에 설치 가능한 최대 슬롯 수
DANGER_RATIO = 0.70
WARNING_RATIO = 0.40


# ── 계산 함수 ──────────────────────────────────────────────
def calc_stats(installed_motors, battery_type, pack_count, max_power_w):
    spec = BATTERY_SPECS[battery_type]
    capacity_mah = spec["capacity_mah"] * pack_count

    current_a = sum(
        MOTOR_SPECS[m]["current_a"] for m in installed_motors if m is not None
    )
    power_w = current_a * ROBOT_VOLTAGE

    runtime_min = None
    if current_a > 0:
        runtime_min = (capacity_mah / 1000 / current_a) * 60

    ratio = power_w / max_power_w if max_power_w > 0 else 0
    if ratio >= DANGER_RATIO:
        status = "danger"
    elif ratio >= WARNING_RATIO:
        status = "warning"
    else:
        status = "safe"

    motor_counts = {"m120": 0, "m300": 0, "servo": 0}
    for m in installed_motors:
        if m is not None:
            motor_counts[m] += 1

    return {
        "capacity_mah": capacity_mah,
        "current_a": current_a,
        "power_w": power_w,
        "runtime_min": runtime_min,
        "status": status,
        "ratio": ratio,
        "motor_counts": motor_counts,
    }


# ── 세션 상태 초기화 ────────────────────────────────────────
if "installed" not in st.session_state:
    st.session_state.installed = [None] * SLOT_COUNT
if "battery_type" not in st.session_state:
    st.session_state.battery_type = "AA"
if "pack_count" not in st.session_state:
    st.session_state.pack_count = 1
if "max_power_w" not in st.session_state:
    st.session_state.max_power_w = 15


# ── 드래그앤드롭 컴포넌트 HTML ──────────────────────────────
def build_drag_drop_component(installed, motor_specs):
    installed_json = json.dumps(installed)
    motor_json = json.dumps(motor_specs)

    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: transparent;
    color: #1e293b;
    user-select: none;
  }}
  .root {{ display: flex; flex-direction: column; gap: 20px; padding: 4px; }}

  /* ── 팔레트 ── */
  .palette-label {{
    font-size: 11px; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: #64748b; margin-bottom: 8px;
  }}
  .palette {{
    display: flex; gap: 12px; flex-wrap: wrap;
  }}
  .motor-chip {{
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    padding: 10px 16px; border-radius: 12px;
    border: 2px solid transparent; cursor: grab;
    font-size: 12px; font-weight: 600; min-width: 80px;
    transition: transform .15s, box-shadow .15s;
    position: relative;
  }}
  .motor-chip:active {{ cursor: grabbing; }}
  .motor-chip:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,.15); }}
  .motor-chip .chip-icon {{ font-size: 22px; }}
  .motor-chip .chip-current {{ font-size: 10px; font-weight: 400; opacity: .75; }}

  .chip-m120  {{ background: #dcfce7; border-color: #86efac; color: #15803d; }}
  .chip-m300  {{ background: #fee2e2; border-color: #fca5a5; color: #b91c1c; }}
  .chip-servo {{ background: #dbeafe; border-color: #93c5fd; color: #1d4ed8; }}

  /* ── 로봇 슬롯 ── */
  .robot-label {{
    font-size: 11px; font-weight: 600; letter-spacing: .08em;
    text-transform: uppercase; color: #64748b; margin-bottom: 8px;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .robot-label span {{ font-weight: 400; font-size: 10px; color: #94a3b8; text-transform: none; letter-spacing: 0; }}
  .slots-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }}
  .slot {{
    height: 80px; border-radius: 12px;
    border: 2px dashed #cbd5e1;
    background: #f8fafc;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 4px; font-size: 11px; color: #94a3b8;
    transition: border-color .15s, background .15s;
    position: relative; cursor: default;
  }}
  .slot.drag-over {{
    border-color: #6366f1; background: #eef2ff;
  }}
  .slot.occupied {{
    border-style: solid; cursor: pointer;
  }}
  .slot.occupied:hover::after {{
    content: "✕";
    position: absolute; top: 4px; right: 6px;
    font-size: 12px; color: #94a3b8; line-height: 1;
  }}
  .slot-motor-icon {{ font-size: 24px; }}
  .slot-motor-label {{ font-size: 10px; font-weight: 600; }}
  .slot-num {{ font-size: 10px; color: #cbd5e1; }}

  .slot-m120  {{ background: #f0fdf4; border-color: #86efac; }}
  .slot-m300  {{ background: #fff1f2; border-color: #fca5a5; }}
  .slot-servo {{ background: #eff6ff; border-color: #93c5fd; }}
</style>
</head>
<body>
<div class="root">

  <div>
    <div class="palette-label">모터 팔레트 — 슬롯으로 드래그하세요</div>
    <div class="palette" id="palette">
      <div class="motor-chip chip-m120"
           draggable="true" data-motor="m120"
           ondragstart="onDragStart(event)">
        <span class="chip-icon">⚡</span>
        <span>120 모터</span>
        <span class="chip-current">0.4 A</span>
      </div>
      <div class="motor-chip chip-m300"
           draggable="true" data-motor="m300"
           ondragstart="onDragStart(event)">
        <span class="chip-icon">🔥</span>
        <span>300 모터</span>
        <span class="chip-current">0.8 A</span>
      </div>
      <div class="motor-chip chip-servo"
           draggable="true" data-motor="servo"
           ondragstart="onDragStart(event)">
        <span class="chip-icon">🎯</span>
        <span>서보 모터</span>
        <span class="chip-current">0.2 A</span>
      </div>
    </div>
  </div>

  <div>
    <div class="robot-label">
      로봇 슬롯 (최대 8개)
      <span>슬롯을 클릭하면 제거</span>
    </div>
    <div class="slots-grid" id="slots-grid"></div>
  </div>

</div>

<script>
const MOTOR_META = {{
  m120:  {{ label: "120 모터", icon: "⚡", cls: "slot-m120"  }},
  m300:  {{ label: "300 모터", icon: "🔥", cls: "slot-m300"  }},
  servo: {{ label: "서보",    icon: "🎯", cls: "slot-servo" }},
}};

let installed = {installed_json};
let dragging = null;

function renderSlots() {{
  const grid = document.getElementById('slots-grid');
  grid.innerHTML = '';
  for (let i = 0; i < {SLOT_COUNT}; i++) {{
    const motor = installed[i];
    const div = document.createElement('div');
    div.className = 'slot' + (motor ? ' occupied ' + MOTOR_META[motor].cls : '');
    div.dataset.index = i;

    if (motor) {{
      div.innerHTML = `
        <span class="slot-motor-icon">${{MOTOR_META[motor].icon}}</span>
        <span class="slot-motor-label">${{MOTOR_META[motor].label}}</span>`;
      div.onclick = () => removeMotor(i);
    }} else {{
      div.innerHTML = `<span class="slot-num">슬롯 ${{i + 1}}</span>`;
    }}

    div.addEventListener('dragover', e => {{ e.preventDefault(); div.classList.add('drag-over'); }});
    div.addEventListener('dragleave', () => div.classList.remove('drag-over'));
    div.addEventListener('drop', e => {{ e.preventDefault(); div.classList.remove('drag-over'); dropMotor(i); }});
    grid.appendChild(div);
  }}
}}

function onDragStart(e) {{
  dragging = e.currentTarget.dataset.motor;
}}

function dropMotor(index) {{
  if (!dragging) return;
  installed[index] = dragging;
  dragging = null;
  renderSlots();
  sendUpdate();
}}

function removeMotor(index) {{
  installed[index] = null;
  renderSlots();
  sendUpdate();
}}

function sendUpdate() {{
  window.parent.postMessage({{
    type: "streamlit:setComponentValue",
    value: JSON.stringify(installed)
  }}, "*");
}}

renderSlots();
</script>
</body>
</html>
"""
    return html


# ── 레이아웃 ────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; max-width: 1100px; }
  h1 { font-size: 1.6rem !important; }
  .stMetric label { font-size: 0.75rem !important; }
  .stMetric [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🤖 프로보 테크닉 — 에너지 과부하 모니터")

# ── 두 컬럼 ──────────────────────────────────────────────
col_left, col_right = st.columns([6, 4], gap="large")

# ── 왼쪽: 드래그앤드롭 ──────────────────────────────────
with col_left:
    st.markdown("#### 모터 배치판")
    component_value = components.html(
        build_drag_drop_component(
            st.session_state.installed,
            MOTOR_SPECS,
        ),
        height=320,
        scrolling=False,
    )

    # postMessage → session_state 동기화
    # (Streamlit custom component 방식으로 처리)
    st.markdown("""
    <script>
    window.addEventListener("message", function(e) {
        if (e.data && e.data.type === "streamlit:setComponentValue") {
            window.parent.postMessage(e.data, "*");
        }
    });
    </script>
    """, unsafe_allow_html=True)

    st.caption("💡 팔레트에서 모터를 드래그해 슬롯에 놓으세요. 슬롯을 클릭하면 제거됩니다.")

    st.markdown("---")

    # ── 수동 편집 폼 (드래그앤드롭 보조) ──
    st.markdown("**⌨️ 직접 입력으로도 설정 가능**")
    c1, c2, c3 = st.columns(3)
    with c1:
        n_m120 = st.number_input("⚡ 120 모터", 0, 8, key="n_m120",
                                 value=st.session_state.installed.count("m120"))
    with c2:
        n_m300 = st.number_input("🔥 300 모터", 0, 8, key="n_m300",
                                 value=st.session_state.installed.count("m300"))
    with c3:
        n_servo = st.number_input("🎯 서보 모터", 0, 8, key="n_servo",
                                  value=st.session_state.installed.count("servo"))

    if st.button("🔄 입력값으로 슬롯 업데이트", use_container_width=True):
        total = n_m120 + n_m300 + n_servo
        if total > SLOT_COUNT:
            st.error(f"슬롯은 최대 {SLOT_COUNT}개입니다. 현재 {total}개 → 줄여주세요.")
        else:
            motors = (["m120"] * n_m120 + ["m300"] * n_m300 +
                      ["servo"] * n_servo + [None] * SLOT_COUNT)
            st.session_state.installed = motors[:SLOT_COUNT]
            st.rerun()


# ── 오른쪽: 설정 + 결과 ──────────────────────────────────
with col_right:
    st.markdown("#### 배터리 설정")

    bat_col1, bat_col2 = st.columns(2)
    with bat_col1:
        battery_type = st.selectbox(
            "종류",
            options=list(BATTERY_SPECS.keys()),
            format_func=lambda k: BATTERY_SPECS[k]["label"],
            index=0 if st.session_state.battery_type == "AA" else 1,
        )
        st.session_state.battery_type = battery_type

    with bat_col2:
        pack_count = st.number_input("팩 수 (1팩=4개)", 1, 10,
                                     value=st.session_state.pack_count)
        st.session_state.pack_count = pack_count

    max_power_w = st.slider(
        "⚙️ 게이지 최대치 (W)", 1, 100,
        value=st.session_state.max_power_w,
    )
    st.session_state.max_power_w = max_power_w

    st.markdown("---")

    # ── 계산 결과 ──────────────────────────────────────
    stats = calc_stats(
        st.session_state.installed,
        st.session_state.battery_type,
        st.session_state.pack_count,
        max_power_w,
    )

    STATUS_CFG = {
        "safe":    {"emoji": "✅", "color": "#16a34a", "label": "안전",  "bg": "#f0fdf4"},
        "warning": {"emoji": "⚠️", "color": "#d97706", "label": "주의",  "bg": "#fffbeb"},
        "danger":  {"emoji": "🚨", "color": "#dc2626", "label": "위험!","bg": "#fff1f2"},
    }
    cfg = STATUS_CFG[stats["status"]]

    st.markdown(f"""
    <div style="background:{cfg['bg']}; border-left:4px solid {cfg['color']};
                border-radius:8px; padding:12px 16px; margin-bottom:16px;">
      <span style="color:{cfg['color']}; font-weight:700; font-size:15px;">
        {cfg['emoji']} {cfg['label']}
      </span>
    </div>
    """, unsafe_allow_html=True)

    # 메트릭 카드
    m1, m2 = st.columns(2)
    m1.metric("소모 전류", f"{stats['current_a']:.2f} A")
    m2.metric("소모 전력", f"{stats['power_w']:.1f} W")

    m3, m4 = st.columns(2)
    m3.metric("배터리 용량", f"{stats['capacity_mah']:,} mAh")

    if stats["runtime_min"] is not None:
        if stats["runtime_min"] >= 60:
            h, m_rem = divmod(int(stats["runtime_min"]), 60)
            time_str = f"{h}시간 {m_rem}분"
        else:
            time_str = f"{stats['runtime_min']:.1f} 분"
    else:
        time_str = "—"
    m4.metric("예상 작동 시간", time_str)

    # 전력 게이지
    pct = min(stats["ratio"] * 100, 100)
    bar_color = cfg["color"]
    st.markdown(f"""
    <div style="margin-top:12px;">
      <div style="display:flex; justify-content:space-between; font-size:12px; color:#64748b; margin-bottom:4px;">
        <span>전력 부하</span>
        <span>{stats['power_w']:.1f} / {max_power_w} W ({pct:.0f}%)</span>
      </div>
      <div style="background:#e2e8f0; border-radius:99px; height:10px;">
        <div style="width:{pct:.1f}%; background:{bar_color};
                    border-radius:99px; height:100%;
                    transition: width .4s ease;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 모터별 분류
    st.markdown("---")
    st.markdown("**현재 설치된 모터**")
    counts = stats["motor_counts"]
    for key, spec in MOTOR_SPECS.items():
        cnt = counts[key]
        cur = cnt * spec["current_a"]
        if cnt > 0:
            st.markdown(
                f"- {spec['icon']} **{spec['label']}** × {cnt} → {cur:.2f} A"
            )
    if all(v == 0 for v in counts.values()):
        st.caption("슬롯에 모터가 없습니다.")

    # 초기화 버튼
    st.markdown("")
    if st.button("🗑️ 전체 슬롯 초기화", use_container_width=True, type="secondary"):
        st.session_state.installed = [None] * SLOT_COUNT
        st.rerun()
