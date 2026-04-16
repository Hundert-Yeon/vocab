import streamlit as st
import streamlit.components.v1 as components

# ── 단어 데이터 ───────────────────────────────────────────────────────────────
WORDS = [
    {"en": "proficiency",   "answers": ["능숙함","숙달","구사능력","능숙"]},
    {"en": "approach",      "answers": ["접근하다","접근","가까워지다","다가가다"]},
    {"en": "internalize",   "answers": ["내면화하다","내면화"]},
    {"en": "outpour",       "answers": ["유출","유출물"]},
    {"en": "decay",         "answers": ["썩다","부패하다","부패","쇠퇴","소멸"]},
    {"en": "assertive",     "answers": ["단정적인","단언적인","자기주장이 강한","독단적인","자기주장"]},
    {"en": "manageable",    "answers": ["다루기 쉬운","제어하기 쉬운","다루기쉬운"]},
    {"en": "circumstance",  "answers": ["환경","상황"]},
    {"en": "severity",      "answers": ["격렬","혹독","심함","심각함"]},
    {"en": "contention",    "answers": ["논점","논쟁"]},
    {"en": "partake",       "answers": ["먹다","마시다"]},
    {"en": "suicide",       "answers": ["자살"]},
    {"en": "circulate",     "answers": ["순환하다","퍼뜨리다","순환"]},
    {"en": "insulation",    "answers": ["절연","단열"]},
    {"en": "ambiguous",     "answers": ["애매한","모호한","불분명한","애매모호한"]},
    {"en": "decisive",      "answers": ["결정적인","확고한","과단성 있는","최종의","명백한","과단성있는"]},
    {"en": "implication",   "answers": ["영향","결과","함축","암시","연루","관계"]},
    {"en": "personalize",   "answers": ["개인화하다","개인화","맞추다","개인의 취향에 맞추다"]},
    {"en": "occasion",      "answers": ["경우","사건","때","기회"]},
    {"en": "adapt",         "answers": ["적응하다","개작하다","적응시키다","개조하다","맞추다","변형하다"]},
    {"en": "casualty",      "answers": ["사상자","피해자"]},
    {"en": "hectic",        "answers": ["매우 바쁜","열광적인","몹시 바쁜","바쁜"]},
    {"en": "waste",         "answers": ["낭비하다","낭비","쓰레기","버려진","쓸모없게 된"]},
    {"en": "confirmation",  "answers": ["확인","승인","일치"]},
    {"en": "monarch",       "answers": ["군주","왕","주권자"]},
    {"en": "casual",        "answers": ["평상시의","격식을 차리지 않는","느긋한","태평스러운","캐주얼"]},
    {"en": "rigor",         "answers": ["엄격함","정확함","엄격"]},
    {"en": "apparel",       "answers": ["의류","옷","의복"]},
    {"en": "precise",       "answers": ["정확한","세심한","정확"]},
    {"en": "respond",       "answers": ["대답하다","답하다","대답"]},
]

TOTAL = len(WORDS)
COLS  = 5
ROWS  = TOTAL // COLS  # 6


# ── 세션 초기화 ───────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "broken":        [False] * TOTAL,
        "selected":      None,
        "feedback":      "",
        "feedback_type": None,
        "input_key":     0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_game():
    st.session_state.broken        = [False] * TOTAL
    st.session_state.selected      = None
    st.session_state.feedback      = ""
    st.session_state.feedback_type = None
    st.session_state.input_key    += 1


def normalize(s: str) -> str:
    return s.strip().replace(" ", "")


def check_answer(idx: int, user_input: str) -> bool:
    return normalize(user_input) in [normalize(a) for a in WORDS[idx]["answers"]]


def select_brick(i: int):
    if st.session_state.broken[i]:
        return
    st.session_state.selected      = i
    st.session_state.feedback      = ""
    st.session_state.feedback_type = None
    st.session_state.input_key    += 1


def submit_answer(raw: str):
    sel = st.session_state.selected
    if sel is None:
        st.session_state.feedback      = "⚠️ 먼저 단어 벽돌을 클릭하세요!"
        st.session_state.feedback_type = "info"
        return
    inp = raw.strip()
    if not inp:
        return
    if check_answer(sel, inp):
        word                           = WORDS[sel]["en"]
        st.session_state.broken[sel]   = True
        st.session_state.selected      = None
        st.session_state.feedback      = f"✅  정답!  '{word}' 벽돌이 깨졌어요!"
        st.session_state.feedback_type = "correct"
    else:
        st.session_state.feedback      = "❌  틀렸어요. 다시 시도해보세요!"
        st.session_state.feedback_type = "wrong"
    st.session_state.input_key += 1


# ── 전역 CSS ──────────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* 앱 배경 */
.stApp { background: #f0f4f8; }
section[data-testid="stMain"] > div { padding-top: 1.2rem; }

/* 타이틀 */
h1 { font-size: 24px !important; font-weight: 800 !important; color: #1e293b !important; }

/* 점수 카드 행 */
.scoreboard { display: flex; gap: 10px; margin: 14px 0 10px; }
.sc {
    flex: 1; background: white;
    border-radius: 12px; padding: 12px 8px;
    text-align: center; border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.sc .n { font-size: 26px; font-weight: 800; color: #1d4ed8; line-height: 1.1; }
.sc .l { font-size: 11px; color: #94a3b8; margin-top: 2px; }

/* 진행바 */
.pw { background: #e2e8f0; border-radius: 100px; height: 9px; overflow: hidden; margin-bottom: 14px; }
.pi { height: 100%; border-radius: 100px; background: #22c55e; transition: width .4s ease; }

/* 피드백 */
.fb { border-radius: 9px; padding: 8px 14px; font-weight: 600; font-size: 13px; margin-bottom: 10px; }
.fb-correct { background:#f0fdf4; border:1px solid #86efac; color:#15803d; }
.fb-wrong   { background:#fff1f2; border:1px solid #fca5a5; color:#b91c1c; }
.fb-info    { background:#fffbeb; border:1px solid #fcd34d; color:#92400e; }

/* 입력 폼 정렬 */
div[data-testid="stForm"] { background: transparent; border: none; padding: 0; }

/* 확인 버튼 */
div[data-testid="stFormSubmitButton"] button {
    background: #1d4ed8 !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    height: 42px;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background: #1e40af !important;
}

/* 텍스트 인풋 */
div[data-testid="stTextInput"] input {
    border-radius: 9px !important;
    border: 1.5px solid #93c5fd !important;
    font-size: 15px !important;
    height: 42px;
}

/* 초기화·다시하기 버튼 */
div[data-testid="stButton"] button {
    border-radius: 9px !important;
    font-weight: 600 !important;
}

/* 완료 배너 */
.done-banner {
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    border-radius: 16px; padding: 28px;
    text-align: center; color: white; margin: 8px 0 18px;
}
.done-banner h2 { font-size: 24px; margin-bottom: 6px; font-weight: 800; }
.done-banner p  { font-size: 14px; opacity: .9; }
</style>
"""

# ── 벽돌 그리드 (iframe-free inline HTML + JS → query param) ─────────────────
def brick_grid_html(broken, selected) -> str:
    cell_h = 60          # px per brick row
    grid_h = ROWS * cell_h + 4

    cells = []
    for i, w in enumerate(WORDS):
        if broken[i]:
            cls   = "b brk"
            label = f"✓ {w['en']}"
        elif selected == i:
            cls   = "b sel"
            label = w["en"]
        else:
            cls   = "b"
            label = w["en"]
        cells.append(
            f'<div class="{cls}" onclick="pick({i})">{label}</div>'
        )

    html = f"""
<style>
.grid {{
    display: grid;
    grid-template-columns: repeat({COLS}, 1fr);
    gap: 0;
    border-radius: 13px;
    overflow: hidden;
    border: 2px solid #bfdbfe;
    box-shadow: 0 2px 8px rgba(0,0,0,.09);
    font-family: -apple-system, sans-serif;
}}
.b {{
    min-height: {cell_h}px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700;
    text-align: center; line-height: 1.3;
    padding: 6px 4px;
    border: 1px solid #bfdbfe;
    cursor: pointer;
    background: #dbeafe;
    color: #1e40af;
    transition: background .1s;
    user-select: none;
    box-sizing: border-box;
}}
.b:hover {{ background: #bfdbfe; }}
.sel {{
    background: #4f46e5 !important;
    color: white !important;
    border-color: #4338ca !important;
    box-shadow: inset 0 0 0 2px #a5b4fc;
}}
.brk {{
    background: #dcfce7 !important;
    color: #166534 !important;
    border-color: #86efac !important;
    opacity: .72;
    cursor: default !important;
    font-weight: 600 !important;
}}
.brk:hover {{ background: #dcfce7 !important; }}
</style>
<div class="grid">{''.join(cells)}</div>
<script>
function pick(i) {{
    const u = new URL(window.parent.location.href);
    u.searchParams.set('sel', i);
    window.parent.location.href = u.toString();
}}
</script>
"""
    return html, grid_h


# ── 메인 ──────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="영어 단어 벽돌깨기",
        page_icon="🧱",
        layout="centered",
    )
    init_state()
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # query param 수신 (벽돌 클릭)
    params = st.query_params
    if "sel" in params:
        try:
            idx = int(params["sel"])
            if 0 <= idx < TOTAL and not st.session_state.broken[idx]:
                select_brick(idx)
        except ValueError:
            pass
        st.query_params.clear()
        st.rerun()

    broken_count = sum(st.session_state.broken)
    score        = round((broken_count / TOTAL) * 100)
    pct          = score
    game_done    = broken_count == TOTAL

    # ── 타이틀 ──
    st.title("🧱 영어 단어 벽돌깨기")
    st.caption("파란 벽돌 클릭 → 한국어 뜻 입력 → 맞추면 벽돌이 깨져요!")

    # ── 점수판 ──
    st.markdown(f"""
    <div class="scoreboard">
      <div class="sc"><div class="n">{score}<span style="font-size:14px">점</span></div><div class="l">현재 점수 / 100점</div></div>
      <div class="sc"><div class="n">{broken_count}<span style="font-size:14px"> / {TOTAL}</span></div><div class="l">맞춘 단어</div></div>
      <div class="sc"><div class="n">{TOTAL - broken_count}</div><div class="l">남은 단어</div></div>
    </div>
    <div class="pw"><div class="pi" style="width:{pct}%"></div></div>
    """, unsafe_allow_html=True)

    # ── 완료 ──
    if game_done:
        st.markdown("""
        <div class="done-banner">
          <h2>🎉 완전 정복!</h2>
          <p>30개 모두 맞혔어요! 최종 점수 <strong>100점 만점!</strong> 🏆</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 처음부터 다시하기", use_container_width=True):
            reset_game()
            st.rerun()
        return

    # ── 선택 안내 ──
    sel = st.session_state.selected
    if sel is not None:
        st.markdown(
            f"<p style='font-size:13px;color:#4f46e5;font-weight:700;margin:0 0 6px'>"
            f"▶ 선택: <u>{WORDS[sel]['en']}</u> — 한국어 뜻을 입력하세요</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<p style='font-size:13px;color:#94a3b8;margin:0 0 6px'>파란 벽돌을 클릭하세요</p>",
            unsafe_allow_html=True,
        )

    # ── 입력 폼 ──
    with st.form(key=f"af_{st.session_state.input_key}", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_input = st.text_input(
                "답",
                placeholder="한국어 뜻 입력 후 Enter 또는 확인",
                label_visibility="collapsed",
            )
        with c2:
            submitted = st.form_submit_button("확인 ✓", use_container_width=True)

    if submitted:
        submit_answer(user_input)
        st.rerun()

    # ── 피드백 ──
    if st.session_state.feedback:
        cls = {
            "correct": "fb-correct",
            "wrong":   "fb-wrong",
            "info":    "fb-info",
        }.get(st.session_state.feedback_type, "fb-info")
        st.markdown(
            f'<div class="fb {cls}">{st.session_state.feedback}</div>',
            unsafe_allow_html=True,
        )

    # ── 벽돌 그리드 ──
    html_str, grid_h = brick_grid_html(st.session_state.broken, st.session_state.selected)
    components.html(html_str, height=grid_h, scrolling=False)

    # ── 초기화 ──
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if st.button("🔄 초기화"):
        reset_game()
        st.rerun()


if __name__ == "__main__":
    main()
