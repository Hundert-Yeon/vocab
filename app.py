import streamlit as st
import random

# ── 단어 데이터 ──────────────────────────────────────────────
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

# ── 세션 초기화 ──────────────────────────────────────────────
def init_state():
    if "broken" not in st.session_state:
        st.session_state.broken = [False] * TOTAL
    if "selected" not in st.session_state:
        st.session_state.selected = None
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""
    if "feedback_ok" not in st.session_state:
        st.session_state.feedback_ok = None
    if "answer_input" not in st.session_state:
        st.session_state.answer_input = ""
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

def reset_game():
    st.session_state.broken = [False] * TOTAL
    st.session_state.selected = None
    st.session_state.feedback = ""
    st.session_state.feedback_ok = None
    st.session_state.answer_input = ""
    st.session_state.input_key += 1

def normalize(s: str) -> str:
    return s.strip().replace(" ", "")

def check_answer(idx: int, user_input: str) -> bool:
    return normalize(user_input) in [normalize(a) for a in WORDS[idx]["answers"]]

def select_brick(idx: int):
    if st.session_state.broken[idx]:
        return
    st.session_state.selected = idx
    st.session_state.feedback = ""
    st.session_state.feedback_ok = None
    st.session_state.answer_input = ""
    st.session_state.input_key += 1

def submit_answer():
    inp = st.session_state.answer_input.strip()
    sel = st.session_state.selected
    if sel is None:
        st.session_state.feedback = "⚠️ 먼저 단어 벽돌을 클릭하세요!"
        st.session_state.feedback_ok = None
        return
    if not inp:
        return
    if check_answer(sel, inp):
        st.session_state.broken[sel] = True
        st.session_state.selected = None
        st.session_state.feedback = f"✅ 정답! '{WORDS[sel]['en']}' 벽돌이 깨졌어요!"
        st.session_state.feedback_ok = True
    else:
        st.session_state.feedback = "❌ 틀렸어요. 다시 시도해보세요!"
        st.session_state.feedback_ok = False
    st.session_state.answer_input = ""
    st.session_state.input_key += 1

# ── CSS ─────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp { background-color: #f8f9fb; }

    /* 점수판 */
    .score-card {
        background: white;
        border-radius: 14px;
        padding: 16px 24px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .score-num { font-size: 32px; font-weight: 700; color: #1a56db; }
    .score-label { font-size: 13px; color: #64748b; margin-top: 2px; }

    /* 벽돌 버튼 */
    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 56px;
        font-size: 13px;
        font-weight: 600;
        border-radius: 10px;
        border: 2px solid #93c5fd;
        background-color: #dbeafe;
        color: #1e40af;
        transition: all 0.15s;
        white-space: normal;
        line-height: 1.3;
        padding: 6px 4px;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #bfdbfe;
        border-color: #3b82f6;
        transform: scale(1.03);
    }

    /* 깨진 벽돌 */
    .broken-brick {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 56px;
        font-size: 13px;
        font-weight: 600;
        border-radius: 10px;
        border: 2px solid #86efac;
        background-color: #dcfce7;
        color: #166534;
        opacity: 0.65;
        text-align: center;
        line-height: 1.3;
        padding: 6px 4px;
    }

    /* 선택된 벽돌 강조 */
    .selected-brick {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 56px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 10px;
        border: 2px solid #7c3aed;
        background-color: #7c3aed;
        color: white;
        text-align: center;
        line-height: 1.3;
        padding: 6px 4px;
        box-shadow: 0 0 0 3px #c4b5fd;
    }

    /* 피드백 */
    .fb-correct {
        background: #f0fdf4;
        border: 1px solid #86efac;
        border-radius: 10px;
        padding: 10px 16px;
        color: #15803d;
        font-weight: 600;
        font-size: 15px;
        text-align: center;
    }
    .fb-wrong {
        background: #fff1f2;
        border: 1px solid #fca5a5;
        border-radius: 10px;
        padding: 10px 16px;
        color: #b91c1c;
        font-weight: 600;
        font-size: 15px;
        text-align: center;
    }
    .fb-info {
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 10px;
        padding: 10px 16px;
        color: #92400e;
        font-weight: 600;
        font-size: 15px;
        text-align: center;
    }

    /* 완료 배너 */
    .complete-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        color: white;
        margin: 16px 0;
    }
    .complete-banner h2 { font-size: 28px; margin-bottom: 8px; }
    .complete-banner p  { font-size: 16px; opacity: 0.9; }

    /* 진행바 */
    .progress-wrap {
        background: #e2e8f0;
        border-radius: 100px;
        height: 12px;
        overflow: hidden;
        margin: 8px 0;
    }
    .progress-inner {
        height: 100%;
        border-radius: 100px;
        background: #1d9e75;
        transition: width 0.4s ease;
    }

    /* 입력창 */
    .stTextInput input {
        border-radius: 10px;
        border: 1.5px solid #93c5fd;
        font-size: 16px;
        padding: 10px 14px;
    }
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px #bfdbfe;
    }

    /* 제출 버튼 */
    .submit-btn > div[data-testid="stButton"] > button {
        background-color: #1a56db !important;
        border-color: #1a56db !important;
        color: white !important;
        font-weight: 700;
        font-size: 15px;
        border-radius: 10px;
        padding: 10px 24px;
    }
    .submit-btn > div[data-testid="stButton"] > button:hover {
        background-color: #1e40af !important;
    }

    /* 타이틀 */
    h1 { color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

# ── 메인 ────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="영어 단어 벽돌깨기", page_icon="🧱", layout="wide")
    init_state()
    inject_css()

    broken_count = sum(st.session_state.broken)
    score = round((broken_count / TOTAL) * 100)
    game_done = broken_count == TOTAL

    # ── 헤더 ──
    st.title("🧱 영어 단어 벽돌깨기")
    st.caption("단어 벽돌을 클릭하고 한국어 뜻을 입력해서 벽돌을 깨세요!")

    # ── 점수판 ──
    col_s1, col_s2, col_s3, col_s4 = st.columns([1, 1, 1, 1])
    with col_s1:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-num">{score}점</div>
            <div class="score-label">현재 점수 (만점 100)</div>
        </div>""", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-num">{broken_count} / {TOTAL}</div>
            <div class="score-label">맞춘 단어 수</div>
        </div>""", unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-num">{TOTAL - broken_count}</div>
            <div class="score-label">남은 단어 수</div>
        </div>""", unsafe_allow_html=True)
    with col_s4:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-num">{'🏆' if game_done else '🎯'}</div>
            <div class="score-label">{'완료!' if game_done else '진행 중'}</div>
        </div>""", unsafe_allow_html=True)

    # ── 진행바 ──
    st.markdown(f"""
    <div style="margin: 16px 0 4px; font-size:13px; color:#64748b;">진행률 {round((broken_count/TOTAL)*100)}%</div>
    <div class="progress-wrap">
        <div class="progress-inner" style="width:{round((broken_count/TOTAL)*100)}%"></div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 완료 배너 ──
    if game_done:
        st.markdown("""
        <div class="complete-banner">
            <h2>🎉 축하합니다! 완전 정복!</h2>
            <p>단어 30개를 모두 맞혔어요! 최종 점수: <strong>100점 만점!</strong> 🏆</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 다시 하기", use_container_width=False):
            reset_game()
            st.rerun()
        return

    # ── 선택 정보 ──
    sel = st.session_state.selected
    if sel is not None:
        st.info(f"**선택된 단어:** `{WORDS[sel]['en']}` — 한국어 뜻을 아래에 입력하세요")
    else:
        st.markdown(
            "<p style='color:#64748b; font-size:14px;'>👇 파란 벽돌을 클릭해서 단어를 선택하세요</p>",
            unsafe_allow_html=True
        )

    # ── 입력창 + 제출 ──
    inp_col, btn_col = st.columns([5, 1])
    with inp_col:
        user_input = st.text_input(
            "한국어 뜻 입력",
            value=st.session_state.answer_input,
            key=f"input_{st.session_state.input_key}",
            placeholder="한국어 뜻을 입력하고 Enter 또는 확인 버튼을 누르세요",
            label_visibility="collapsed",
        )
        st.session_state.answer_input = user_input
    with btn_col:
        st.markdown('<div class="submit-btn">', unsafe_allow_html=True)
        if st.button("확인 ✓", use_container_width=True):
            submit_answer()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Enter키 제출 처리
    if user_input and user_input != st.session_state.get("_last_input", ""):
        st.session_state["_last_input"] = user_input

    # ── 피드백 ──
    if st.session_state.feedback:
        fb = st.session_state.feedback
        ok = st.session_state.feedback_ok
        css_cls = "fb-correct" if ok is True else ("fb-wrong" if ok is False else "fb-info")
        st.markdown(f'<div class="{css_cls}">{fb}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── 벽돌 그리드 (5열) ──
    COLS = 5
    rows = [WORDS[i:i+COLS] for i in range(0, TOTAL, COLS)]
    idx = 0
    for row in rows:
        cols = st.columns(COLS)
        for c, word in zip(cols, row):
            with c:
                i = idx
                if st.session_state.broken[i]:
                    st.markdown(
                        f'<div class="broken-brick">✓ {word["en"]}</div>',
                        unsafe_allow_html=True
                    )
                elif st.session_state.selected == i:
                    st.markdown(
                        f'<div class="selected-brick">▶ {word["en"]}</div>',
                        unsafe_allow_html=True
                    )
                    if st.button(f"선택됨", key=f"brick_{i}"):
                        select_brick(i)
                        st.rerun()
                else:
                    if st.button(word["en"], key=f"brick_{i}"):
                        select_brick(i)
                        st.rerun()
            idx += 1

    st.divider()
    col_r1, col_r2 = st.columns([6, 1])
    with col_r2:
        if st.button("🔄 초기화", use_container_width=True):
            reset_game()
            st.rerun()

if __name__ == "__main__":
    main()
