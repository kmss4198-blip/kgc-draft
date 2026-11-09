import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="정관장 드래프트 1~10위 전체 예측전", page_icon="🏀", layout="wide")

# --- 데이터 저장/불러오기 함수 ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

participants = load_data()
MAX_PARTICIPANTS = 5
current_count = len(participants)

# 1. 헤더 영역
st.caption("정관장 레드부스터스")
st.title("🏀 드래프트 1~10위 전체 순위 예측전")
st.write("각 참가자가 1위부터 10위까지 지명될 선수 목록을 예측하고 5명의 결과를 한눈에 비교해보세요!")

# 2. 참가 현황
st.subheader(f"참가 현황: {current_count} / {MAX_PARTICIPANTS}명")

# 3. 탭 구성 (등록 / 수정·삭제 / 전체 비교)
tab1, tab2, tab3 = st.tabs(["💳 새 카드 만들기", "✏️ 기존 제출 수정 / 삭제", "📊 5인 전체 예측 비교"])

# ----- 탭 1: 새 카드 만들기 -----
with tab1:
    if current_count < MAX_PARTICIPANTS:
        with st.form("prediction_form", clear_on_submit=True):
            name = st.text_input("닉네임", placeholder="닉네임을 입력하세요")
            st.write("---")
            st.write("### 🎯 1위 ~ 10위 지명 예측 선수 입력")
            
            # 2열(Column)로 나누어 입력 폼 배치
            col1, col2 = st.columns(2)
            preds = {}
            
            with col1:
                for i in range(1, 6):
                    preds[str(i)] = st.text_input(f"{i}순위 예측 선수", key=f"new_rank_{i}")
            with col2:
                for i in range(6, 11):
                    preds[str(i)] = st.text_input(f"{i}순위 예측 선수", key=f"new_rank_{i}")

            submit = st.form_submit_button("1~10위 예측 제출하기")
            
            if submit:
                existing_names = [p["name"] for p in participants]
                if not name.strip():
                    st.warning("닉네임을 입력해 주세요.")
                elif name in existing_names:
                    st.warning("이미 등록된 닉네임입니다. '수정/삭제' 탭을 이용해 주세요.")
                elif any(not v.strip() for v in preds.values()):
                    st.warning("1위부터 10위까지 모든 순위의 선수 이름을 입력해 주세요.")
                else:
                    participants.append({"name": name, "predictions": preds})
                    save_data(participants)
                    st.success(f"{name}님의 1~10위 예측 카드가 등록되었습니다!")
                    st.rerun()
    else:
        st.warning("⚠️ 5명 정원이 모두 완료되었습니다. '수정/삭제' 탭을 이용해 주세요.")

# ----- 탭 2: 기존 제출 수정 및 삭제 -----
with tab2:
    if not participants:
        st.info("현재 등록된 참가자가 없습니다.")
    else:
        names = [p["name"] for p in participants]
        selected_name = st.selectbox("본인 닉네임 선택", names)
        
        target_p = next(p for p in participants if p["name"] == selected_name)
        
        with st.form("edit_form"):
            st.write(f"**{selected_name}** 님의 1~10위 예측 정보를 수정합니다.")
            col1, col2 = st.columns(2)
            new_preds = {}
            
            with col1:
                for i in range(1, 6):
                    new_preds[str(i)] = st.text_input(
                        f"{i}순위 예측 선수", 
                        value=target_p["predictions", {}].get(str(i), ""), 
                        key=f"edit_rank_{i}"
                    )
            with col2:
                for i in range(6, 11):
                    new_preds[str(i)] = st.text_input(
                        f"{i}순위 예측 선수", 
                        value=target_p["predictions", {}].get(str(i), ""), 
                        key=f"edit_rank_{i}"
                    )
            
            btn_edit = st.form_submit_button("수정 완료")
            
            if btn_edit:
                if any(not v.strip() for v in new_preds.values()):
                    st.warning("1위부터 10위까지 모든 선수를 입력해 주세요.")
                else:
                    target_p["predictions"] = new_preds
                    save_data(participants)
                    st.success(f"{selected_name}님의 예측이 수정되었습니다!")
                    st.rerun()
        
        st.write("---")
        if st.button(f"🗑️ '{selected_name}' 참가 정보 삭제하기"):
            participants = [p for p in participants if p["name"] != selected_name]
            save_data(participants)
            st.success(f"{selected_name}님의 참가 정보가 삭제되었습니다.")
            st.rerun()

# ----- 탭 3: 5인 전체 예측 비교 -----
with tab3:
    if not participants:
        st.info("아직 등록된 참가자가 없습니다.")
    else:
        st.write("### 📋 5인 전체 1~10위 예측 현황표")
        
        # DataFrame을 생성하여 1~10위 비교 표 출력
        table_data = {"순위": [f"{i}순위" for i in range(1, 11)]}
        for p in participants:
            table_data[p["name"]] = [p["predictions", {}].get(str(i), "-") for i in range(1, 11)]
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
