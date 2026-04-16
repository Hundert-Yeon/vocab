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
ROWS  = TOTAL // COLS


def init_state():
    defaults = {
        "broken":        [False] * TOTAL,
        "feedback":      "",
        "feedback_type": None,
        "last_broken":   None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_game():
    st.session_state.broken        = [False] * TOTAL
    st.session_state.feedback      = ""
    st.session_state.feedback_type = None
    st.session_state.last_broken   = None


def normalize(s):
    return s.strip().replace(" ", "")


def find_and_break(raw):
    inp = normalize(raw)
    if not inp:
        return
    for i, w in enumerate(WORDS):
        if st.session_state.broken[i]:
            continue
        if inp in [normalize(a) for a in w["answers"]]:
            st.session_state.broken[i]     = True
            st.session_state.last_broken   = i
            st.session_state.feedback      = f"✅  정답!  '{w['en']}' 벽돌이 깨졌어요!"
            st.session_state.feedback_type = "correct"
            return
    st.session_state.last_broken   = None
    st.session_state.feedback      = f"❌  '{raw.strip()}'은(는) 해당하는 단어가 없어요!"
    st.session_state.feedback_type = "wrong"


GLOBAL_CSS = """
<style>
.stApp { background: #f0f4f8; }
section[data-testid="stMain"] > div { padding-top: 1.2rem; }
h1 { font-size: 24px !important; font-weight: 800 !important; color: #1e293b !important; }

.scoreboard { display: flex; gap: 10px; margin: 14px 0 10px; }
.sc {
    flex: 1; background: white; border-radius: 12px; padding: 12px 8px;
    text-align: center; border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.sc .n { font-size: 26px; font-weight: 800; color: #1d4ed8; line-height: 1.1; }
.sc .l { font-size: 11px; color: #94a3b8; margin-top: 2px; }

.pw { background: #e2e8f0; border-radius: 100px; height: 9px; overflow: hidden; margin-bottom: 14px; }
.pi { height: 100%; border-radius: 100px; background: #22c55e; transition: width .4s ease; }

.guide {
    font-size: 13px; color: #4f46e5; font-weight: 600;
    margin: 0 0 8px; padding: 7px 12px;
    background: #eef2ff; border-radius: 8px;
    border-left: 3px solid #4f46e5;
}

.fb { border-radius: 9px; padding: 8px 14px; font-weight: 600; font-size: 13px; margin: 6px 0 4px; }
.fb-correct { background:#f0fdf4; border:1px solid #86efac; color:#15803d; }
.fb-wrong   { background:#fff1f2; border:1px solid #fca5a5; color:#b91c1c; }

div[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; }

div[data-testid="stTextInput"] input {
    border-radius: 9px !important;
    border: 1.5px solid #93c5fd !important;
    font-size: 15px !important;
    height: 42px;
}
div[data-testid="stFormSubmitButton"] button {
    background: #1d4ed8 !important; color: white !important;
    border: none !important; border-radius: 9px !important;
    font-weight: 700 !important; font-size: 14px !important;
    height: 42px; width: 100%;
}
div[data-testid="stFormSubmitButton"] button:hover { background: #1e40af !important; }
div[data-testid="stButton"] button { border-radius: 9px !important; font-weight: 600 !important; }

.done-banner {
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    border-radius: 16px; padding: 28px;
    text-align: center; color: white; margin: 8px 0 18px;
}
.done-banner h2 { font-size: 24px; margin-bottom: 6px; font-weight: 800; }
.done-banner p  { font-size: 14px; opacity: .9; }
</style>
"""


def brick_grid_html(broken, last_broken):
    cell_h = 62
    grid_h = ROWS * cell_h + 6

    cells = []
    for i, w in enumerate(WORDS):
        if broken[i]:
            extra = " new" if i == last_broken else ""
            cells.append(f'<div class="b brk{extra}">✓ {w["en"]}</div>')
        else:
            cells.append(f'<div class="b">{w["en"]}</div>')

    html = f"""
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
@keyframes pulse{{
  0%{{transform:scale(1);background:#dcfce7;}}
  40%{{transform:scale(1.09);background:#86efac;}}
  100%{{transform:scale(1);background:#dcfce7;}}
}}
.grid{{
    display:grid;
    grid-template-columns:repeat({COLS},1fr);
    gap:0;
    border-radius:13px;
    overflow:hidden;
    border:2px solid #bfdbfe;
    box-shadow:0 2px 8px rgba(0,0,0,.09);
    font-family:-apple-system,sans-serif;
}}
.b{{
    min-height:{cell_h}px;
    display:flex;align-items:center;justify-content:center;
    font-size:12px;font-weight:700;
    text-align:center;line-height:1.3;
    padding:6px 4px;
    border:1px solid #bfdbfe;
    background:#dbeafe;
    color:#1e40af;
    user-select:none;
}}
.brk{{
    background:#dcfce7!important;
    color:#166534!important;
    border-color:#86efac!important;
    opacity:.75;
    font-weight:600!important;
}}
.brk.new{{
    opacity:1;
    animation:pulse .55s ease;
}}
</style>
<div class="grid">{''.join(cells)}</div>
"""
    return html, grid_h


def main():
    st.set_page_config(page_title="영어 단어 벽돌깨기", page_icon="🧱", layout="centered")
    init_state()
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    broken_count = sum(st.session_state.broken)
    score        = round((broken_count / TOTAL) * 100)
    game_done    = broken_count == TOTAL

    st.title("🧱 영어 단어 벽돌깨기")
    st.caption("한국어 뜻을 입력하면 해당 단어 벽돌이 자동으로 깨져요!")

    st.markdown(f"""
    <div class="scoreboard">
      <div class="sc">
        <div class="n">{score}<span style="font-size:14px">점</span></div>
        <div class="l">현재 점수 / 100점</div>
      </div>
      <div class="sc">
        <div class="n">{broken_count}<span style="font-size:14px"> / {TOTAL}</span></div>
        <div class="l">맞춘 단어</div>
      </div>
      <div class="sc">
        <div class="n">{TOTAL - broken_count}</div>
        <div class="l">남은 단어</div>
      </div>
    </div>
    <div class="pw"><div class="pi" style="width:{score}%"></div></div>
    """, unsafe_allow_html=True)

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

    st.markdown(
        '<div class="guide">💡 한국어 뜻을 입력하면 맞는 벽돌이 자동으로 깨집니다. 벽돌을 클릭하지 않아도 돼요!</div>',
        unsafe_allow_html=True,
    )

    with st.form(key="answer_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_input = st.text_input(
                "답",
                placeholder="한국어 뜻 입력 후 Enter 또는 확인  (예: 능숙함, 접근하다 …)",
                label_visibility="collapsed",
            )
        with c2:
            submitted = st.form_submit_button("확인 ✓", use_container_width=True)

    if submitted:
        find_and_break(user_input)
        st.rerun()

    if st.session_state.feedback:
        cls = "fb-correct" if st.session_state.feedback_type == "correct" else "fb-wrong"
        st.markdown(
            f'<div class="fb {cls}">{st.session_state.feedback}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    html_str, grid_h = brick_grid_html(st.session_state.broken, st.session_state.last_broken)
    components.html(html_str, height=grid_h, scrolling=False)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("🔄 초기화"):
        reset_game()
        st.rerun()


if __name__ == "__main__":
    main()
