import streamlit as st
from datetime import date

from services.auth_service import get_current_user
from services.exercise_service import get_exercises
from services.workout_service import (
    create_workout_session,
    create_workout_record,
    create_workout_set
)
from services.routine_service import (
    get_user_routines,
    get_routine_items
)


st.title("🏋️ 운동 기록 입력")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다. 먼저 로그인해주세요.")
    st.stop()

user_id = user.id

workout_date = st.date_input("운동 날짜", value=date.today())

input_mode = st.radio(
    "입력 방식 선택",
    ["개별 운동 입력", "루틴 단위 입력"]
)

st.divider()

if input_mode == "개별 운동 입력":
    exercise_list = get_exercises()

    if not exercise_list:
        st.info("등록된 운동 종목이 없습니다.")
        st.stop()

    exercise_options = {
        exercise["exercise_name"]: exercise["exercise_id"]
        for exercise in exercise_list
    }

    selected_exercise_name = st.selectbox(
        "운동 선택",
        list(exercise_options.keys())
    )

    selected_exercise_id = exercise_options[selected_exercise_name]

    weight = st.number_input("중량(kg)", min_value=0.0, step=1.0)
    reps = st.number_input("반복 횟수", min_value=0, step=1)
    sets = st.number_input("세트 수", min_value=1, step=1)
    difficulty = st.slider("운동 난이도", 1, 10, 5)
    memo = st.text_area("메모")

    if st.button("운동 기록 저장", type="primary"):
        session_result = create_workout_session(
            user_id=user_id,
            routine_id=None,
            workout_date=str(workout_date)
        )

        if not session_result["success"]:
            st.error(session_result["error"])
            st.stop()

        session_id = session_result["data"]["session_id"]

        record_result = create_workout_record(
            session_id=session_id,
            exercise_id=selected_exercise_id
        )

        if not record_result["success"]:
            st.error(record_result["error"])
            st.stop()

        record_id = record_result["data"]["workout_record_id"]

        for set_number in range(1, int(sets) + 1):
            set_result = create_workout_set(
                record_id=record_id,
                set_number=set_number,
                weight=float(weight),
                reps=int(reps)
            )

            if not set_result["success"]:
                st.warning(set_result["error"])

        st.success("✅ 운동 기록이 저장되었습니다!")
        st.write("운동 날짜:", workout_date)
        st.write("운동 종목:", selected_exercise_name)
        st.write("중량:", weight)
        st.write("반복 횟수:", reps)
        st.write("세트 수:", sets)
        st.write("난이도:", difficulty)
        st.write("메모:", memo)
        st.balloons()


else:
    routines = get_user_routines(user_id)

    if not routines:
        st.info("등록된 루틴이 없습니다. 먼저 Routine View에서 루틴을 생성해주세요.")
        st.stop()

    routine_options = {
        routine["routine_name"]: routine["routine_id"]
        for routine in routines
    }

    selected_routine_name = st.selectbox(
        "루틴 선택",
        list(routine_options.keys())
    )

    selected_routine_id = routine_options[selected_routine_name]

    routine_items = get_routine_items(selected_routine_id)

    if not routine_items:
        st.warning("선택한 루틴에 포함된 운동이 없습니다.")
        st.stop()

    st.subheader("루틴 운동 기록 수정")

    st.info("루틴 기본값을 불러왔습니다. 오늘 실제 수행한 세트/반복/중량으로 수정한 뒤 저장하세요.")

    edited_items = []

    for idx, item in enumerate(routine_items, 1):
        exercise_data = item.get("exercises")
        exercise_name = "운동명 없음"

        if isinstance(exercise_data, dict):
            exercise_name = exercise_data.get("exercise_name", "운동명 없음")

        default_sets = int(item.get("target_sets") or 1)
        default_reps = int(item.get("target_reps") or 1)
        default_weight = float(item.get("target_weight") or 0)

        with st.container(border=True):
            st.write(f"### {idx}. {exercise_name}")

            do_exercise = st.checkbox(
                "오늘 이 운동 수행",
                value=True,
                key=f"do_exercise_{idx}_{item.get('routine_item_id')}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                actual_sets = st.number_input(
                    "실제 세트 수",
                    min_value=1,
                    max_value=30,
                    value=default_sets,
                    step=1,
                    key=f"actual_sets_{idx}_{item.get('routine_item_id')}"
                )

            with col2:
                actual_reps = st.number_input(
                    "실제 반복 횟수",
                    min_value=1,
                    max_value=100,
                    value=default_reps,
                    step=1,
                    key=f"actual_reps_{idx}_{item.get('routine_item_id')}"
                )

            with col3:
                actual_weight = st.number_input(
                    "실제 중량(kg)",
                    min_value=0.0,
                    max_value=500.0,
                    value=default_weight,
                    step=1.0,
                    key=f"actual_weight_{idx}_{item.get('routine_item_id')}"
                )

            if do_exercise:
                edited_items.append({
                    "exercise_id": item.get("exercise_id"),
                    "exercise_name": exercise_name,
                    "sets": actual_sets,
                    "reps": actual_reps,
                    "weight": actual_weight
                })

    memo = st.text_area("루틴 운동 메모")

    if st.button("루틴 운동 기록 저장", type="primary"):
        if not edited_items:
            st.warning("저장할 운동이 없습니다. 최소 1개 이상의 운동을 선택해주세요.")
            st.stop()

        session_result = create_workout_session(
            user_id=user_id,
            routine_id=selected_routine_id,
            workout_date=str(workout_date)
        )

        if not session_result["success"]:
            st.error(session_result["error"])
            st.stop()

        session_id = session_result["data"]["session_id"]

        has_error = False

        for item in edited_items:
            record_result = create_workout_record(
                session_id=session_id,
                exercise_id=item["exercise_id"]
            )

            if not record_result["success"]:
                has_error = True
                st.warning(record_result["error"])
                continue

            record_id = record_result["data"]["workout_record_id"]

            for set_number in range(1, int(item["sets"]) + 1):
                set_result = create_workout_set(
                    record_id=record_id,
                    set_number=set_number,
                    weight=float(item["weight"]),
                    reps=int(item["reps"])
                )

                if not set_result["success"]:
                    has_error = True
                    st.warning(set_result["error"])

        if not has_error:
            st.success("✅ 루틴 단위 운동 기록이 저장되었습니다!")
            st.write("운동 날짜:", workout_date)
            st.write("선택 루틴:", selected_routine_name)

            st.write("### 저장된 운동")
            for item in edited_items:
                st.write(
                    f"- {item['exercise_name']}: "
                    f"{item['sets']}세트 × {item['reps']}회 × {item['weight']}kg"
                )

            st.balloons()
        else:
            st.warning("일부 운동 기록 저장 중 문제가 발생했습니다.")