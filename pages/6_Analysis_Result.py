import streamlit as st

from services.auth_service import get_current_user
from services.analysis_service import (
    get_simple_analysis,
    get_analysis_history
)


st.title("📊 분석 결과 조회")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다. 먼저 로그인해주세요.")
    st.stop()

user_id = user.id

analysis = get_simple_analysis(user_id)

if not analysis:
    st.info("아직 분석할 운동 기록이 없습니다.")
    st.stop()

st.subheader("최신 운동 분석")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("운동 날짜", analysis.get("workout_date", "N/A"))

with col2:
    st.metric("총 운동량", f'{analysis.get("total_volume", 0):.0f} kg')

with col3:
    st.metric("분석 상태", analysis.get("status", "N/A"))

st.divider()

st.subheader("운동 정보")

exercise_names = analysis.get("exercise_names", [])

if exercise_names:
    for name in exercise_names:
        st.write(f"- {name}")
else:
    st.write("운동 종목 정보가 없습니다.")

st.divider()

st.subheader("회복 상태")

fatigue = analysis.get("fatigue")
condition = analysis.get("condition")

col1, col2 = st.columns(2)

with col1:
    st.metric("전체 피로도", fatigue if fatigue is not None else "N/A")

with col2:
    st.metric("전체 컨디션", condition if condition is not None else "N/A")

status = analysis.get("status")
message = analysis.get("message")

if status == "회복 부족":
    st.error(message)
elif status == "주의 필요":
    st.warning(message)
elif status == "회복 양호":
    st.success(message)
else:
    st.info(message)

st.divider()

st.subheader("최근 운동 세션")

history = get_analysis_history(user_id, limit=10)

if history:
    for idx, session in enumerate(history, 1):
        with st.container(border=True):
            st.write(f"**#{idx} 운동 세션**")
            st.write(f"세션 ID: {session.get('session_id')}")
            st.write(f"운동 날짜: {session.get('workout_date')}")
            st.write(f"생성일: {session.get('created_at', 'N/A')}")
else:
    st.info("최근 운동 이력이 없습니다.")