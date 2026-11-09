import json
import os
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="정관장 레드부스터스 드래프트 예측전", page_icon="🏀")

# --- 파일 기반 공용 데이터 저장 로직 ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 공용 데이터 불러오기
participants = load_data()
MAX_PARTICIPANTS = 5
current_count = len(participants)

# 1. 헤더 영역
st.caption("정관장 레드부스터스")
st.title("드래프트 예측전 🏀")
st.write("정관장이 뽑을 추첨 순위와 지명 선수를 맞히는 게임입니다 (선착순 순위 지정).")

# 2. 참가자 수 상태 표시
st.subheader(f"참가 현황: {current_count} / {MAX_PARTICIPANTS}")

# 이미 선점된 순위 목록
taken_ranks = [p["rank"] for p in participants]

# 3. 1~10번 순위 보드 시각화
st.write("### 🎯 순위별 선점 현황 (1~10위)")
cols = st.columns(10)
for i in range(1, 11):
    with cols[i - 1]:
        if i in taken_ranks:
            st.error(f"**{i}**")
        else:
            st.success(f"**{i}**")

st.divider()

# 4. 내 카드 만들기
if current_count < MAX_PARTICIPANTS:
    st.write("### 💳 내 카드 만들기")
    with st.form("prediction_form", clear_on_submit=True):
        name = st.text_input("닉네임", placeholder="닉네임을 입력하세요")
        available_ranks = [r for r in range(1, 11) if r not in taken_ranks]
        rank = st.selectbox("예측 순위 선택", available_ranks)
        player = st.text_input("지명 예측 선수 이름", placeholder="선수 이름을 입력하세요")
        
        submit = st.form_submit_button("예측 제출하기")
        
        if submit:
            if not name.strip() or not player.strip():
                st.warning("닉네임과 선수 이름을 모두 입력해 주세요.")
            else:
                participants.append({"name": name, "rank": rank, "player": player})
                save_data(participants) # 파일에 저장하여 모두가 공유
                st.success(f"{name}님! {rank}순위({player}) 예측이 등록되었습니다.")
                st.rerun()
else:
    st.warning("⚠️ 5명 정원이 모두 완료되었습니다.")

# 5. 참가자 현황 출력
st.divider()
st.write("### 📋 등록된 참가자 카드")
if not participants:
    st.info("아직 참가자가 없습니다.")
else:
    for p in participants:
        st.write(f"👤 **{p['name']}** ➔ {p['rank']}순위 ({p['player']})")
