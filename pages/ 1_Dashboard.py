import streamlit as st

from services.auth_service import get_current_user
from services.analysis_service import (
    get_simple_analysis,
    get_latest_recommendation,
    get_analysis_history
)

st.title("🏠 대시보드")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

analysis = get_simple_analysis(user_id)
recommendation = get_latest_recommendation(user_id)

st.subheader("📊 오늘의 요약")

if not analysis:
    st.info("아직 운동 기록이 없습니다.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.write("### 📅 최근 운동일")
        st.write(f"**{analysis.get('workout_date', 'N/A')}**")

with col2:
    with st.container(border=True):
        st.write("### 🏋️ 총 운동량")
        st.write(f"**{analysis.get('total_volume', 0):.0f} kg**")

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.write("### 📌 현재 상태")
        st.write(f"**{analysis.get('status', 'N/A')}**")

with col4:
    with st.container(border=True):
        st.write("### 🎯 추천 강도")
        if recommendation:
            st.write(f"**{recommendation.get('intensity', 'N/A')}**")
        else:
            st.write("**N/A**")

st.divider()

st.subheader("🏋️ 최근 운동 정보")

with st.container(border=True):
    st.write(f"**운동 날짜:** {analysis.get('workout_date', 'N/A')}")
    st.write(f"**총 운동량:** {analysis.get('total_volume', 0):.0f} kg")

    exercise_names = analysis.get("exercise_names", [])

    if exercise_names:
        st.write("**운동 종목:**")
        for name in exercise_names:
            st.write(f"- {name}")
    else:
        st.write("운동 종목 정보가 없습니다.")

st.divider()

st.subheader("🩹 회복 상태")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.write("### 전체 피로도")
        st.write(f"**{analysis.get('fatigue', 'N/A')} / 10**")

with col2:
    with st.container(border=True):
        st.write("### 전체 컨디션")
        st.write(f"**{analysis.get('condition', 'N/A')} / 10**")

status = analysis.get("status")
message = analysis.get("message", "")

if status == "회복 부족":
    st.error(message)
elif status == "주의 필요":
    st.warning(message)
elif status == "회복 양호":
    st.success(message)
else:
    st.info(message)

st.divider()

st.subheader("🎯 오늘의 추천")

if recommendation:
    st.write(f"### {recommendation.get('title', '추천 없음')}")
    st.write(recommendation.get("recommendation", "추천 내용이 없습니다."))
    st.write(f"**추천 근거:** {recommendation.get('reason', 'N/A')}")

    used_muscles = recommendation.get("used_muscles", [])
    if used_muscles:
        st.write("**최근 사용 근육:**")
        st.write(", ".join(used_muscles))

    recommended_exercises = recommendation.get("recommended_exercises", [])
    if recommended_exercises:
        st.write("**추천 운동:**")
        for exercise in recommended_exercises:
            st.write(f"- {exercise}")
else:
    st.info("추천 결과가 없습니다.")

st.divider()

st.subheader("📈 최근 운동 세션")

history = get_analysis_history(user_id, limit=5)

if history:
    for idx, session in enumerate(history, 1):
        with st.container(border=True):
            st.write(f"**#{idx} 운동 세션**")
            st.write(f"세션 ID: {session.get('session_id')}")
            st.write(f"운동 날짜: {session.get('workout_date')}")
            st.write(f"생성일: {session.get('created_at', 'N/A')}")
else:
    st.info("최근 운동 이력이 없습니다.")

st.divider()

st.subheader("⚡ 빠른 이동")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💪 운동 기록 입력", use_container_width=True):
        st.switch_page("pages/3_Workout_Input.py")

with col2:
    if st.button("🩹 회복 기록 입력", use_container_width=True):
        st.switch_page("pages/4_Recovery_Input.py")

with col3:
    if st.button("📊 분석 결과 보기", use_container_width=True):
        st.switch_page("pages/6_Analysis_Result.py")

with col4:
    if st.button("🎯 추천 결과 보기", use_container_width=True):
        st.switch_page("pages/7_Recommendation_View.py")