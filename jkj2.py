import json
import os
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="정관장 레드부스터스 1~10위 드래프트 예측전", page_icon="🏀", layout="wide")

# --- 정관장 레드부스터스 붉은색 테마 커스텀 CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #4A0000 100%);
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #ffffff !important;
    }
    div[data-testid="stForm"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div[data-testid="stForm"] label, div[data-testid="stForm"] p {
        color: #1a1a1a !important;
        font-weight: bold;
    }
    div[data-testid="stForm"] select, div[data-testid="stForm"] input {
        border: 1px solid #cc0000 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 8px 8px 0 0;
        color: #ffffff !important;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #8B0000 !important;
        font-weight: bold;
    }
    div[data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 🏀 드래프트 참가 선수 명단 (원하는 선수 이름으로 수정하세요)
# =========================================================
DRAFT_PLAYERS = [
    "선택하세요",
    "김도은", "이원석", "문정현", "박무빈", "유기상",
    "조준희", "신주영", "박승재", "이우석", "허웅",
    "허훈", "최준용", "송교창", "강상재", "양홍석",
    "이관희", "변준형", "오세근", "김선형", "정효근"
]

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
st.caption("🔴 KGC KOREA GINSENG CORPORATION")
st.title("🏀 정관장 레드부스터스 1~10위 드래프트 예측전")
st.write("5명이서 각자 1순위부터 10순위까지의 지명 선수를 드롭다운 목록에서 선택하고 비교해보세요!")

st.markdown(f"### 👥 현재 참가 현황: **{current_count} / {MAX_PARTICIPANTS}명**")

st.divider()

# 2. 탭 메뉴 구획
tab1, tab2 = st.tabs(["💳 내 1~10위 예측 제출 / 수정", "📊 5인 전체 예측 현황표"])

# ----- 탭 1: 입력 및 수정 -----
with tab1:
    names = [p["name"] for p in participants]
    mode = st.radio("작업 선택", ["새로 제출하기", "기존 예측 수정 / 삭제"], horizontal=True)
    
    if mode == "새로 제출하기":
        if current_count >= MAX_PARTICIPANTS:
            st.warning("⚠️ 이미 5명이 모두 참가를 완료했습니다. 수정이나 삭제는 '기존 예측 수정 / 삭제'를 이용해 주세요.")
        else:
            with st.form("new_prediction_form", clear_on_submit=True):
                name = st.text_input("닉네임 입력", placeholder="예: 농구왕")
                st.write("---")
                st.write("🎯 **1위 ~ 10위 지명 예측 선수 선택 (목록에서 선택)**")
                
                col1, col2 = st.columns(2)
                preds = {}
                with col1:
                    for i in range(1, 6):
                        preds[str(i)] = st.selectbox(
                            f"{i}순위 예측 선수", 
                            options=DRAFT_PLAYERS, 
                            key=f"new_{i}"
                        )
                with col2:
                    for i in range(6, 11):
                        preds[str(i)] = st.selectbox(
                            f"{i}순위 예측 선수", 
                            options=DRAFT_PLAYERS, 
                            key=f"new_{i}"
                        )
                
                submit = st.form_submit_button("1~10위 예측 제출하기")
                
                if submit:
                    selected_vals = list(preds.values())
                    if not name.strip():
                        st.warning("닉네임을 입력해 주세요.")
                    elif name in names:
                        st.warning("이미 등록된 닉네임입니다.")
                    elif "선택하세요" in selected_vals:
                        st.warning("1위부터 10위까지 모든 순위의 선수를 선택해 주세요.")
                    elif len(set(selected_vals)) < 10:
                        st.warning("⚠️ 한 선수를 중복으로 여러 순위에 선택할 수 없습니다. 서로 다른 선수를 선택해 주세요.")
                    else:
                        participants.append({"name": name, "predictions": preds})
                        save_data(participants)
                        st.success(f"{name}님의 1~10위 예측 결과가 저장되었습니다!")
                        st.rerun()
                        
    else: # 기존 예측 수정 / 삭제
        if not participants:
            st.info("현재 등록된 참가자가 없습니다.")
        else:
            selected_name = st.selectbox("본인 닉네임 선택", names)
            target_p = next(p for p in participants if p["name"] == selected_name)
            preds_dict = target_p.get("predictions", {})
            
            with st.form("edit_prediction_form"):
                st.write(f"✏️ **'{selected_name}'** 님의 1~10위 예측 수정")
                col1, col2 = st.columns(2)
                new_preds = {}
                with col1:
                    for i in range(1, 6):
                        curr_val = preds_dict.get(str(i), "선택하세요")
                        idx = DRAFT_PLAYERS.index(curr_val) if curr_val in DRAFT_PLAYERS else 0
                        new_preds[str(i)] = st.selectbox(
                            f"{i}순위 예측 선수", 
                            options=DRAFT_PLAYERS, 
                            index=idx, 
                            key=f"edit_{i}"
                        )
                with col2:
                    for i in range(6, 11):
                        curr_val = preds_dict.get(str(i), "선택하세요")
                        idx = DRAFT_PLAYERS.index(curr_val) if curr_val in DRAFT_PLAYERS else 0
                        new_preds[str(i)] = st.selectbox(
                            f"{i}순위 예측 선수", 
                            options=DRAFT_PLAYERS, 
                            index=idx, 
                            key=f"edit_{i}"
                        )
                
                btn_edit = st.form_submit_button("수정 내용 저장")
                if btn_edit:
                    selected_vals = list(new_preds.values())
                    if "선택하세요" in selected_vals:
                        st.warning("1위부터 10위까지 모든 순위의 선수를 선택해 주세요.")
                    elif len(set(selected_vals)) < 10:
                        st.warning("⚠️ 한 선수를 중복으로 여러 순위에 선택할 수 없습니다.")
                    else:
                        target_p["predictions"] = new_preds
                        save_data(participants)
                        st.success(f"{selected_name}님의 예측 정보가 수정되었습니다!")
                        st.rerun()
            
            st.write("---")
            if st.button(f"🗑️ '{selected_name}' 예측 카드 완전 삭제"):
                participants = [p for p in participants if p["name"] != selected_name]
                save_data(participants)
                st.success("삭제되었습니다.")
                st.rerun()

# ----- 탭 2 현황표 -----
with tab2:
    st.write("### 📋 5인 전체 1~10위 예측 현황표")
    if not participants:
        st.info("아직 등록된 참가자가 없습니다.")
    else:
        table_data = {"순위": [f"{i}순위" for i in range(1, 11)]}
        for p in participants:
            preds_dict = p.get("predictions", {})
            table_data[p["name"]] = [preds_dict.get(str(i), "-") for i in range(1, 11)]
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

# 하단 상시 현황표
st.divider()
st.write("### 📋 5인 전체 1~10위 실시간 예측 비교표")
if not participants:
    st.info("아직 예측을 제출한 참가자가 없습니다.")
else:
    table_data = {"순위": [f"{i}순위" for i in range(1, 11)]}
    for p in participants:
        preds_dict = p.get("predictions", {})
        table_data[p["name"]] = [preds_dict.get(str(i), "-") for i in range(1, 11)]
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
