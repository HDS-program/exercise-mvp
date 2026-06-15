import streamlit as st
from datetime import date

from services.auth_service import get_current_user
from services.exercise_service import get_exercises
from services.workout_service import (
    create_workout_session,
    create_workout_record,
    create_workout_set
)


st.title("🏋️ 운동 기록 입력")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다. 먼저 로그인해주세요.")
    st.stop()

user_id = user.id

exercise_list = get_exercises()

if not exercise_list:
    st.info("등록된 운동 종목이 없습니다.")
    st.stop()

exercise_options = {
    exercise["exercise_name"]: exercise["exercise_id"]
    for exercise in exercise_list
}

workout_date = st.date_input("운동 날짜", value=date.today())

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

    for set_number in range(1, sets + 1):
        set_result = create_workout_set(
            record_id=record_id,
            set_number=set_number,
            weight=weight,
            reps=reps
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