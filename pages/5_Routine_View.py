import streamlit as st

from services.auth_service import get_current_user
from services.exercise_service import get_all_exercises
from services.routine_service import (
    get_user_routines,
    get_routine_items,
    create_routine,
    add_routine_item,
    delete_routine
)


st.title("📋 루틴 조회 및 생성")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

tab1, tab2 = st.tabs(["루틴 조회", "루틴 생성"])

with tab1:
    routines = get_user_routines(user_id)

    if not routines:
        st.info("등록된 루틴이 없습니다.")
    else:
        st.subheader(f"총 {len(routines)}개의 루틴")

        routine_options = {
            r.get("routine_name", "이름 없음"): r
            for r in routines
        }

        selected_name = st.selectbox(
            "루틴 선택",
            list(routine_options.keys())
        )

        selected_routine = routine_options[selected_name]
        routine_id = selected_routine.get("routine_id")

        st.write(f"**루틴명:** {selected_routine.get('routine_name')}")
        st.write(f"**활성화:** {'활성' if selected_routine.get('is_active') else '비활성'}")

        st.subheader("포함된 운동")

        items = get_routine_items(routine_id)

        if items:
            for idx, item in enumerate(items, 1):
                exercise_data = item.get("exercises")
                exercise_name = "운동명 없음"

                if isinstance(exercise_data, dict):
                    exercise_name = exercise_data.get("exercise_name", "운동명 없음")

                with st.container(border=True):
                    st.write(f"### {idx}. {exercise_name}")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("세트", item.get("target_sets", "N/A"))

                    with col2:
                        st.metric("반복", item.get("target_reps", "N/A"))

                    with col3:
                        st.metric("중량", f'{item.get("target_weight", 0)} kg')
        else:
            st.info("이 루틴에 포함된 운동이 없습니다.")

        st.divider()

        if st.button("🗑️ 선택한 루틴 삭제", type="secondary"):
            result = delete_routine(routine_id)

            if result["success"]:
                st.success("루틴이 삭제되었습니다.")
                st.rerun()
            else:
                st.error(result["error"])

with tab2:
    st.subheader("새 루틴 생성")

    exercises = get_all_exercises()

    if not exercises:
        st.info("등록된 운동 종목이 없습니다. 먼저 운동 종목을 추가해주세요.")
        st.stop()

    exercise_options = {
        exercise.get("exercise_name"): exercise.get("exercise_id")
        for exercise in exercises
        if exercise.get("exercise_name") and exercise.get("exercise_id")
    }

    routine_name = st.text_input("루틴명", placeholder="예: 가슴데이, 등데이, 하체데이")

    st.write("### 운동 구성")

    item_count = st.number_input(
        "루틴에 넣을 운동 개수",
        min_value=1,
        max_value=8,
        value=3,
        step=1
    )

    routine_items = []

    for i in range(1, item_count + 1):
        with st.container(border=True):
            st.write(f"**운동 {i}**")

            selected_exercise_name = st.selectbox(
                "운동 선택",
                list(exercise_options.keys()),
                key=f"exercise_{i}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                target_sets = st.number_input(
                    "목표 세트 수",
                    min_value=1,
                    max_value=20,
                    value=3,
                    step=1,
                    key=f"sets_{i}"
                )

            with col2:
                target_reps = st.number_input(
                    "목표 반복 횟수",
                    min_value=1,
                    max_value=100,
                    value=10,
                    step=1,
                    key=f"reps_{i}"
                )

            with col3:
                target_weight = st.number_input(
                    "목표 중량(kg)",
                    min_value=0.0,
                    max_value=500.0,
                    value=0.0,
                    step=1.0,
                    key=f"weight_{i}"
                )

            routine_items.append({
                "exercise_id": exercise_options[selected_exercise_name],
                "exercise_name": selected_exercise_name,
                "target_sets": target_sets,
                "target_reps": target_reps,
                "target_weight": target_weight,
                "item_order": i
            })

    if st.button("✅ 루틴 저장", type="primary"):
        if not routine_name.strip():
            st.warning("루틴명을 입력해주세요.")
            st.stop()

        routine_result = create_routine(
            user_id=user_id,
            routine_name=routine_name.strip(),
            is_active=True
        )

        if not routine_result["success"]:
            st.error(routine_result["error"])
            st.stop()

        routine_id = routine_result["data"]["routine_id"]

        has_error = False

        for item in routine_items:
            item_result = add_routine_item(
                routine_id=routine_id,
                exercise_id=item["exercise_id"],
                target_sets=item["target_sets"],
                target_reps=item["target_reps"],
                target_weight=item["target_weight"],
                item_order=item["item_order"]
            )

            if not item_result["success"]:
                has_error = True
                st.warning(item_result["error"])

        if not has_error:
            st.success("✅ 루틴이 저장되었습니다.")
            st.balloons()
            st.rerun()