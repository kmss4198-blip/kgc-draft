import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. 페이지 및 테마 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="정관장 레드부스터스 드래프트 예측전",
    page_icon="🏀",
    layout="centered"
)

# 이미지의 레드/블랙 UI 테마를 적용하는 Custom CSS
st.markdown("""
<style>
    /* 전체 배경색: 정관장 레드 */
    .stApp {
        background-color: #C8102E;
        color: #ffffff;
    }
    
    /* 상단 대화 상자 모드 안내 */
    .preview-mode {
        background-color: #ffffff;
        color: #333333;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 13px;
        margin-bottom: 20px;
    }
    
    /* 일정 안내 카드 */
    .schedule-box {
        background-color: #141414;
        border: 2px solid #282828;
        border-radius: 14px;
        padding: 16px;
        color: #ffffff;
        margin-bottom: 16px;
    }
    .schedule-box h5 {
        color: #888888;
        font-size: 13px;
        margin-bottom: 8px;
    }
    .schedule-box p {
        font-size: 16px;
        font-weight: bold;
        margin: 0;
    }

    /* 흰색 패널 섹션 (순위별 예측 / 참가자 입력) */
    .white-panel {
        background-color: #ffffff;
        color: #111111;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* 순위 동그라미 아이콘 */
    .rank-badge {
        display: inline-block;
        width: 36px;
        height: 36px;
        line-height: 34px;
        border-radius: 50%;
        border: 2px dashed #333;
        text-align: center;
        font-weight: bold;
        color: #111111;
        margin-right: 8px;
    }
    
    /* 참가자 등록 카드 */
    .participant-card {
        background-color: #1e1e1e;
        color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 5px solid #C8102E;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 드래프트 지명 후보 선수 데이터 세트
# ---------------------------------------------------------
PLAYERS_DATA = [
    {"선수명": "이주영", "학교": "연세대", "포지션": "G", "신장": 189},
    {"선수명": "이동근", "학교": "고려대", "포지션": "F", "신장": 198},
    {"선수명": "문유현", "학교": "고려대", "포지션": "G", "신장": 181},
    {"선수명": "이유진", "학교": "연세대", "포지션": "F", "신장": 200},
    {"선수명": "윤기찬", "학교": "고려대", "포지션": "F", "신장": 194},
    {"선수명": "강지훈", "학교": "연세대", "포지션": "C", "신장": 202},
    {"선수명": "이규태", "학교": "연세대", "포지션": "F/C", "신장": 199},
    {"선수명": "임동일", "학교": "드래프트 재도전", "포지션": "C", "신장": 215},
    {"선수명": "김보배", "학교": "연세대", "포지션": "C", "신장": 202},
    {"선수명": "박정웅", "학교": "홍대부고", "포지션": "G", "신장": 192},
    {"선수명": "이근준", "학교": "경복고", "포지션": "F", "신장": 197},
    {"선수명": "여찬영", "학교": "건국대", "포지션": "G", "신장": 184},
]

df_players = pd.DataFrame(PLAYERS_DATA)

# 드롭다운 표시용 옵션 리스트 ("선수명 (학교, 포지션)")
player_options = ["선택 안 함"] + [
    f"{row['선수명']} ({row['학교']}, {row['포지션']})" 
    for _, row in df_players.iterrows()
]

# ---------------------------------------------------------
# 3. 세션 상태 초기화 (참가자 저장용)
# ---------------------------------------------------------
if "participants" not in st.session_state:
    st.session_state.participants = []

# ---------------------------------------------------------
# 4. 헤더 및 타임라인 UI
# ---------------------------------------------------------
st.markdown('<span style="background:#000; color:#fff; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:12px;">정관장 레드부스터스</span>', unsafe_allow_html=True)
st.markdown("<h1 style='color:white; margin-top:8px; font-size:38px;'>드래프트 예측전</h1>", unsafe_allow_html=True)
st.write("정관장이 뽑을 추첨 순위와, 그 순위로 가장 먼저 지명할 선수를 맞히는 게임입니다.")

st.markdown("""
<div class="preview-mode">
    📌 <b>미리보기 모드입니다.</b> 입력한 내용은 이 기기에만 저장되며 다른 참가자와 실시간 공유되지 않습니다.
</div>
""", unsafe_allow_html=True)

# 지명 일정 박스 2개
col_sch1, col_sch2 = st.columns(2)
with col_sch1:
    st.markdown("""
    <div class="schedule-box">
        <h5>순위 추첨 · 11/9(월)</h5>
        <p>결과 대기 중</p>
    </div>
    """, unsafe_allow_html=True)

with col_sch2:
    st.markdown("""
    <div class="schedule-box">
        <h5>드래프트 첫 지명 · 11/20(금)</h5>
        <p>결과 대기 중</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. 1~10순위 지명 예측 드롭다운 폼
# ---------------------------------------------------------
st.markdown("### 🏀 1~10순위 지명 선수 예측하기")

with st.form("draft_predict_form"):
    nickname = st.text_input("참가자 닉네임", placeholder="닉네임을 입력하세요 (예: 레드부스터스팬)")
    
    st.write("각 순위별 지명될 후보 선수를 드롭다운에서 선택해 주세요.")
    
    user_picks = {}
    
    # 2열로 1~10순위 드롭다운 배치
    cols = st.columns(2)
    for rank in range(1, 11):
        col_idx = (rank - 1) % 2
        with cols[col_idx]:
            user_picks[f"{rank}순위"] = st.selectbox(
                f"⚙️ {rank}순위 지명 선수",
                options=player_options,
                key=f"rank_{rank}"
            )
            
    submit_button = st.form_submit_button("내 카드 만들기 🎟️", use_container_width=True)

    if submit_button:
        # 입력 검증
        if not nickname.strip():
            st.error("닉네임을 입력해 주세요!")
        else:
            selected_list = [v for k, v in user_picks.items() if v != "선택 안 함"]
            
            # 중복 체크
            if len(selected_list) != len(set(selected_list)):
                st.warning("⚠️ 동일한 선수를 여러 순위에 중복해서 선택할 수 없습니다.")
            elif len(selected_list) < 10:
                st.warning("⚠️ 1순위부터 10순위까지 모든 선수를 선택해 주세요.")
            else:
                # 참가자 데이터 저장
                st.session_state.participants.append({
                    "nickname": nickname,
                    "picks": user_picks
                })
                st.success(f"🎉 '{nickname}' 님의 드래프트 예측 카드가 등록되었습니다!")

# ---------------------------------------------------------
# 6. 참가자 예측 카드 목록 출력
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 👥 참가자 예측 카드")

if not st.session_state.participants:
    st.markdown("""
    <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; color: #666; text-align: center;">
        🤖 아직 참가자가 없습니다. 위 폼에서 닉네임과 예측을 입력해 카드를 만들어 보세요!
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, p in enumerate(st.session_state.participants):
        with st.expander(f"👤 {p['nickname']} 님의 1~10순위 예측 카드", expanded=True):
            # 5개씩 2줄로 순위 결과 표시
            row1_cols = st.columns(5)
            for r in range(1, 6):
                with row1_cols[r-1]:
                    player_name = p['picks'][f"{r}순위"].split(" (")[0]
                    st.metric(label=f"{r}순위", value=player_name)
                    
            row2_cols = st.columns(5)
            for r in range(6, 11):
                with row2_cols[r-6]:
                    player_name = p['picks'][f"{r}순위"].split(" (")[0]
                    st.metric(label=f"{r}순위", value=player_name)
