import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="정관장 레드부스터스 드래프트 예측전", page_icon="🏀", layout="wide")

# --- 데이터 저장/불러오기 ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

participants = load_data()
MAX_PARTICIPANTS = 5
current_count = len(participants)

# 1. 헤더 영역
st.caption("정관장 레드부스터스")
st.title("🏀 드래프트 통합 예측전")
st.write("정관장의 추첨 순위/선수 예측과 1~10위 전체 지명 순서 예측을 함께 진행합니다!")

# 2. 참가 현황
st.subheader(f"참가 현황: {current_count} / {MAX_PARTICIPANTS}명")

# 이미 선점된 정관장 순위 목록
taken_kgc_ranks = [p.get("kgc_rank") for p in participants if p.get("kgc_rank") is not None]

# 3. 탭 메뉴 구획
tab1, tab2, tab3 = st.tabs(["💳 내 예측 제출 / 수정", "🎯 정관장 순위별 예측 보드", "📊 1~10위 전체 예측 비교"])

# ----- 탭 1: 내 예측 제출 및 수정 -----
with tab1:
    names = [p["name"] for p in participants]
    user_mode = st.radio("작업 선택", ["새로 참가하기", "기존 예측 수정 / 삭제"], horizontal=True)
    
    if user_mode == "새로 참가하기":
        if current_count >= MAX_PARTICIPANTS:
            st.warning("⚠️ 5명 정원이 모두 완료되었습니다. 기존 제출자는 '기존 예측 수정/삭제'를 이용해 주세요.")
        else:
            with st.form("new_form", clear_on_submit=True):
                name = st.text_input("닉네임", placeholder="닉네임을 입력하세요")
                
                st.markdown("---")
                st.subheader("1️⃣ 정관장 추첨 순위 & 첫 지명 선수 예측 (선착순)")
                available_kgc_ranks = [r for r in range(1, 11) if r not in taken_kgc_ranks]
                kgc_rank = st.selectbox("정관장 예상 추첨 순위 선택 (1~10위)", available_kgc_ranks)
                kgc_player = st.text_input("정관장이 이 순위로 지명할 선수 이름", placeholder="예: 김도은")
                
                st.markdown("---")
                st.subheader("2️⃣ 1위 ~ 10위 전체 지명 선수 예측")
                col1, col2 = st.columns(2)
                preds = {}
                with col1:
                    for i in range(1, 6):
                        preds[str(i)] = st.text_input(f"{i}순위 지명 선수", key=f"new_all_{i}")
                with col2:
                    for i in range(6, 11):
                        preds[str(i)] = st.text_input(f"{i}순위 지명 선수", key=f"new_all_{i}")
                
                submit = st.form_submit_button("모든 예측 제출하기")
                
                if submit:
                    if not name.strip():
                        st.warning("닉네임을 입력해 주세요.")
                    elif name in names:
                        st.warning("이미 등록된 닉네임입니다.")
                    elif not kgc_player.strip():
                        st.warning("정관장 지명 예상 선수를 입력해 주세요.")
                    elif any(not v.strip() for v in preds.values()):
                        st.warning("1위부터 10위까지 모든 순위의 선수 이름을 입력해 주세요.")
                    else:
                        participants.append({
                            "name": name,
                            "kgc_rank": kgc_rank,
                            "kgc_player": kgc_player,
                            "predictions": preds
                        })
                        save_data(participants)
                        st.success(f"{name}님의 예측 카드가 성공적으로 등록되었습니다!")
                        st.rerun()

    else: # 기존 예측 수정/삭제
        if not participants:
            st.info("현재 등록된 참가자가 없습니다.")
        else:
            selected_name = st.selectbox("본인 닉네임 선택", names)
            target_p = next(p for p in participants if p["name"] == selected_name)
            
            my_current_kgc_rank = target_p.get("kgc_rank", 1)
            available_kgc_edit = sorted([r for r in range(1, 11) if r not in taken_kgc_ranks or r == my_current_kgc_rank])
            preds_dict = target_p.get("predictions", {})

            with st.form("edit_form"):
                st.write(f"**'{selected_name}'** 님의 예측 정보를 수정합니다.")
                
                st.markdown("---")
                st.subheader("1️⃣ 정관장 추첨 순위 & 첫 지명 선수 수정")
                new_kgc_rank = st.selectbox(
                    "정관장 예상 추첨 순위", 
                    available_kgc_edit, 
                    index=available_kgc_edit.index(my_current_kgc_rank) if my_current_kgc_rank in available_kgc_edit else 0
                )
                new_kgc_player = st.text_input("정관장 지명 예상 선수", value=target_p.get("kgc_player", ""))
                
                st.markdown("---")
                st.subheader("2️⃣ 1위 ~ 10위 전체 지명 선수 수정")
                col1, col2 = st.columns(2)
                new_preds = {}
                with col1:
                    for i in range(1, 6):
                        new_preds[str(i)] = st.text_input(
                            f"{i}순위 지명 선수", 
                            value=preds_dict.get(str(i), ""), 
                            key=f"edit_all_{i}"
                        )
                with col2:
                    for i in range(6, 11):
                        new_preds[str(i)] = st.text_input(
                            f"{i}순위 지명 선수", 
                            value=preds_dict.get(str(i), ""), 
                            key=f"edit_all_{i}"
                        )
                
                btn_edit = st.form_submit_button("수정 완료")
                if btn_edit:
                    if not new_kgc_player.strip():
                        st.warning("정관장 지명 선수 이름을 입력해 주세요.")
                    elif any(not v.strip() for v in new_preds.values()):
                        st.warning("1~10위 선수를 모두 입력해 주세요.")
                    else:
                        target_p["kgc_rank"] = new_kgc_rank
                        target_p["kgc_player"] = new_kgc_player
                        target_p["predictions"] = new_preds
                        save_data(participants)
                        st.success(f"{selected_name}님의 정보가 수정되었습니다!")
                        st.rerun()
            
            st.markdown("---")
            if st.button(f"🗑️ '{selected_name}' 참가 정보 삭제"):
                participants = [p for p in participants if p["name"] != selected_name]
                save_data(participants)
                st.success("참가 정보가 삭제되었습니다.")
                st.rerun()

# ----- 탭 2: 정관장 순위별 예측 보드 (맨 처음 디자인 원본) -----
with tab2:
    st.write("### 📌 정관장 추첨 순위별 선점 현황 (1~10위)")
    st.caption("선착순으로 정관장의 추첨 순위와 지명 선수를 지정한 현황입니다.")
    
    # 1~10위 아이콘 보드
    cols = st.columns(10)
    for i in range(1, 11):
        matching_p = next((p for p in participants if p.get("kgc_rank") == i), None)
        with cols[i - 1]:
            if matching_p:
                st.error(f"**{i}순위**\n\n👤 {matching_p['name']}")
            else:
                st.success(f"**{i}순위**\n\n(선택 가능)")

    st.markdown("---")
    st.write("### 👥 정관장 예측 참가자 카드 현황")
    if not participants:
        st.info("아직 참가자가 없습니다.")
    else:
        for p in participants:
            r = p.get("kgc_rank", "-")
            player = p.get("kgc_player", "-")
            st.info(f"👤 **{p['name']}** ➔ 정관장 **{r}순위** 지명 예측: **{player}**")

# ----- 탭 3: 1~10위 전체 예측 비교 -----
with tab3:
    st.write("### 📋 5인 전체 1~10위 지명 예측 비교표")
    if not participants:
        st.info("아직 참가자가 없습니다.")
    else:
        table_data = {"순위": [f"{i}순위" for i in range(1, 11)]}
        for p in participants:
            preds_dict = p.get("predictions", {})
            table_data[p["name"]] = [preds_dict.get(str(i), "-") for i in range(1, 11)]
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
