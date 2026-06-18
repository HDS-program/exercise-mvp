import streamlit as st

from services.auth_service import get_current_user
from services.analysis_service import (
    get_simple_analysis,
    get_latest_recommendation,
    save_recommendation_action
)
from services.supabase_client import supabase


def get_muscle_names_for_exercise(exercise_name: str) -> list:
    """
    운동명으로 해당 운동의 target muscle 목록 조회
    """
    try:
        exercise_response = supabase.table("exercises") \
            .select("exercise_id") \
            .eq("exercise_name", exercise_name) \
            .limit(1) \
            .execute()

        if not exercise_response.data:
            return []

        exercise_id = exercise_response.data[0]["exercise_id"]

        target_response = supabase.table("exercise_target_muscles") \
            .select("target_type, muscle_groups(muscle_name)") \
            .eq("exercise_id", exercise_id) \
            .execute()

        if not target_response.data:
            return []

        muscles = []

        for row in target_response.data:
            muscle_data = row.get("muscle_groups")
            target_type = row.get("target_type", "")

            if isinstance(muscle_data, dict):
                muscle_name = muscle_data.get("muscle_name")
                if muscle_name:
                    if target_type == "primary":
                        muscles.append(f"{muscle_name} (주)")
                    else:
                        muscles.append(f"{muscle_name} (보조)")

        return muscles

    except Exception as e:
        print(f"추천 운동 부위 조회 실패: {str(e)}")
        return []


st.title("🎯 추천 결과 조회")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다. 먼저 로그인해주세요.")
    st.stop()

user_id = user.id

analysis = get_simple_analysis(user_id)
recommendation = get_latest_recommendation(user_id)

if not analysis:
    st.info("아직 추천을 생성할 운동 기록이 없습니다.")
    st.stop()

st.subheader("현재 상태 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("최근 운동일", analysis.get("workout_date", "N/A"))

with col2:
    st.metric("전체 피로도", analysis.get("fatigue", "N/A"))

with col3:
    st.metric("전체 컨디션", analysis.get("condition", "N/A"))

st.divider()

st.subheader("추천 결과")

if not recommendation:
    st.info("추천 결과를 생성할 수 없습니다.")
    st.stop()

title = recommendation.get("title", "추천 없음")
content = recommendation.get("recommendation", "추천 내용이 없습니다.")
intensity = recommendation.get("intensity", "N/A")
reason = recommendation.get("reason", "추천 근거가 없습니다.")
recommended_exercises = recommendation.get("recommended_exercises", [])
used_muscles = recommendation.get("used_muscles", [])

if title == "휴식 추천":
    st.error(f"### 🛌 {title}")
elif title == "가벼운 운동 추천":
    st.warning(f"### 🏃 {title}")
elif title == "정상 운동 가능":
    st.success(f"### 💪 {title}")
else:
    st.info(f"### ℹ️ {title}")

st.write(content)

st.metric("추천 운동 강도", intensity)

st.divider()

st.subheader("최근 사용 근육")

if used_muscles:
    st.write("최근 운동에서 사용된 근육 부위입니다. 추천에서는 이 부위를 우선적으로 제외합니다.")
    st.write(", ".join(used_muscles))
else:
    st.info("최근 사용 근육 정보를 찾을 수 없습니다.")

st.divider()

st.subheader("추천 운동")

if recommended_exercises:
    for idx, exercise in enumerate(recommended_exercises, 1):
        muscles = get_muscle_names_for_exercise(exercise)

        with st.container(border=True):
            st.write(f"### {idx}. {exercise}")

            if muscles:
                st.write("**추천 운동 부위**")
                for muscle in muscles:
                    st.write(f"- {muscle}")
            else:
                st.write("운동 부위 정보가 없습니다.")

            st.caption("최근 사용한 근육 부위를 피해서 추천된 운동입니다.")
else:
    st.info("추천할 운동 종목이 없습니다.")

st.divider()

st.subheader("추천 근거")

status = analysis.get("status")
fatigue = analysis.get("fatigue")
condition = analysis.get("condition")
total_volume = analysis.get("total_volume", 0)
exercise_names = analysis.get("exercise_names", [])

st.write(f"**분석 상태:** {status}")
st.write(f"**추천 이유:** {reason}")
st.write(f"**총 운동량:** {total_volume:.0f} kg")

if exercise_names:
    st.write("**최근 수행 운동:**")
    for name in exercise_names:
        st.write(f"- {name}")

st.write(f"**피로도:** {fatigue}")
st.write(f"**컨디션:** {condition}")

st.divider()

st.subheader("사용자 선택")

col1, col2 = st.columns(2)

with col1:
    if st.button("👍 추천 수락", type="primary"):
        result = save_recommendation_action(
            user_id=user_id,
            action_type="accepted",
            action_score=1
        )

        if result["success"]:
            st.success("추천을 수락했습니다. 선택 기록이 저장되었습니다.")
        else:
            st.error(result["error"])

with col2:
    if st.button("👎 추천 거절"):
        result = save_recommendation_action(
            user_id=user_id,
            action_type="rejected",
            action_score=-1
        )

        if result["success"]:
            st.info("추천을 거절했습니다. 선택 기록이 저장되었습니다.")
        else:
            st.error(result["error"])