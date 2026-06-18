import streamlit as st

from services.auth_service import get_current_user
from services.routine_service import (
    get_user_routines,
    get_routine_items,
    add_exercise_to_routine_by_name
)
from services.analysis_service import (
    get_simple_analysis,
    get_latest_recommendation,
    save_recommendation_action
)


st.set_page_config(
    page_title="Exercise MVP",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ 운동 효율 분석 시스템")
st.write("데이터 기반 운동 의사결정 지원 시스템")

user = get_current_user()

if not user:
    st.info("로그인 후 운동 루틴, 분석 결과, 추천 운동을 확인할 수 있습니다.")

    if st.button("🔐 로그인하러 가기", type="primary"):
        st.switch_page("pages/0_Login.py")

    st.stop()

user_id = user.id

st.success("로그인 상태입니다. 오늘의 루틴과 추천 운동을 확인하세요.")

st.divider()

st.subheader("📌 오늘의 운동 루틴 선택")

routines = get_user_routines(user_id)
selected_routine_id = None
selected_routine_name = None

if not routines:
    st.info("등록된 루틴이 없습니다. 먼저 루틴을 생성해주세요.")

    if st.button("📋 루틴 생성하러 가기", type="primary"):
        st.switch_page("pages/5_Routine_View.py")

else:
    routine_options = {
        routine.get("routine_name", "이름 없는 루틴"): routine
        for routine in routines
    }

    selected_routine_name = st.selectbox(
        "오늘 진행할 루틴을 선택하세요",
        list(routine_options.keys())
    )

    selected_routine = routine_options[selected_routine_name]
    selected_routine_id = selected_routine.get("routine_id")

    st.session_state["today_routine_id"] = selected_routine_id
    st.session_state["today_routine_name"] = selected_routine_name

    st.write(f"### ✅ 오늘 선택한 루틴: {selected_routine_name}")

    routine_items = get_routine_items(selected_routine_id)

    if routine_items:
        st.write("#### 루틴 구성")

        for idx, item in enumerate(routine_items, 1):
            exercise_data = item.get("exercises")
            exercise_name = "운동명 없음"

            if isinstance(exercise_data, dict):
                exercise_name = exercise_data.get("exercise_name", "운동명 없음")

            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write(f"**{idx}. {exercise_name}**")

                with col2:
                    st.metric("목표 세트", item.get("target_sets", "N/A"))

                with col3:
                    st.metric("목표 반복", item.get("target_reps", "N/A"))

                with col4:
                    st.metric("목표 중량", f'{item.get("target_weight", 0)} kg')
    else:
        st.warning("선택한 루틴에 포함된 운동이 없습니다.")

st.divider()

st.subheader("📊 현재 운동 분석 상태")

analysis = get_simple_analysis(user_id)

if not analysis:
    st.info("아직 분석할 운동 기록이 없습니다. 운동 기록과 회복 기록을 입력하면 분석 결과가 표시됩니다.")
else:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("최근 운동일", analysis.get("workout_date", "N/A"))

    with col2:
        st.metric("총 운동량", f'{analysis.get("total_volume", 0):.0f} kg')

    with col3:
        st.metric("피로도", analysis.get("fatigue", "N/A"))

    with col4:
        st.metric("컨디션", analysis.get("condition", "N/A"))

    status = analysis.get("status", "N/A")
    message = analysis.get("message", "")

    if status == "회복 부족":
        st.error(f"**{status}** - {message}")
    elif status == "주의 필요":
        st.warning(f"**{status}** - {message}")
    elif status == "회복 양호":
        st.success(f"**{status}** - {message}")
    else:
        st.info(f"**{status}** - {message}")

st.divider()

st.subheader("🎯 오늘의 추천 운동")

recommendation = get_latest_recommendation(user_id)

if not recommendation:
    st.info("추천 결과를 생성할 수 없습니다.")
else:
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
    st.write(f"**추천 강도:** {intensity}")
    st.write(f"**추천 근거:** {reason}")

    if used_muscles:
        st.write("**최근 사용 근육:**")
        st.write(", ".join(used_muscles))

    st.write("#### 추천 운동 상세 설정")

    selected_recommendations = []

    if recommended_exercises:
        for idx, exercise in enumerate(recommended_exercises, start=1):
            with st.container(border=True):
                st.write(f"### {idx}. {exercise}")

                add_exercise = st.checkbox(
                    "이 운동을 루틴에 추가",
                    value=True,
                    key=f"add_recommend_{idx}_{exercise}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    target_sets = st.number_input(
                        "목표 세트",
                        min_value=1,
                        max_value=20,
                        value=3,
                        step=1,
                        key=f"recommend_sets_{idx}_{exercise}"
                    )

                with col2:
                    target_reps = st.number_input(
                        "목표 반복",
                        min_value=1,
                        max_value=100,
                        value=10,
                        step=1,
                        key=f"recommend_reps_{idx}_{exercise}"
                    )

                with col3:
                    target_weight = st.number_input(
                        "목표 중량(kg)",
                        min_value=0.0,
                        max_value=500.0,
                        value=0.0,
                        step=2.5,
                        key=f"recommend_weight_{idx}_{exercise}"
                    )

                if add_exercise:
                    selected_recommendations.append({
                        "exercise_name": exercise,
                        "target_sets": target_sets,
                        "target_reps": target_reps,
                        "target_weight": target_weight
                    })
    else:
        st.info("추천할 운동 종목이 없습니다.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 추천 반영", type="primary", use_container_width=True):
            action_result = save_recommendation_action(
                user_id=user_id,
                action_type="accepted",
                action_score=1
            )

            if not action_result["success"]:
                st.error(action_result["error"])
                st.stop()

            if selected_routine_id is None:
                st.warning("추천을 반영할 루틴이 없습니다. 먼저 오늘 루틴을 선택하거나 생성해주세요.")
                st.stop()

            if not selected_recommendations:
                st.warning("반영할 추천 운동을 선택해주세요.")
                st.stop()

            added_count = 0

            for exercise in selected_recommendations:
                result = add_exercise_to_routine_by_name(
                    routine_id=selected_routine_id,
                    exercise_name=exercise["exercise_name"],
                    target_sets=exercise["target_sets"],
                    target_reps=exercise["target_reps"],
                    target_weight=exercise["target_weight"]
                )

                if result["success"]:
                    added_count += 1
                else:
                    st.warning(result["error"])

            if added_count > 0:
                st.success(f"추천 운동 {added_count}개를 '{selected_routine_name}' 루틴에 추가했습니다.")
                st.rerun()
            else:
                st.info("새로 추가된 추천 운동이 없습니다.")

    with col2:
        if st.button("👎 추천 미반영", use_container_width=True):
            result = save_recommendation_action(
                user_id=user_id,
                action_type="rejected",
                action_score=-1
            )

            if result["success"]:
                st.info("추천 운동을 반영하지 않도록 기록했습니다.")
            else:
                st.error(result["error"])

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
    if st.button("📖 운동 기록 조회", use_container_width=True):
        st.switch_page("pages/8_Workout_History.py")