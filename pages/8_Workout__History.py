import streamlit as st

from services.auth_service import get_current_user
from services.workout_service import (
    get_workout_history,
    get_session_workout_records,
    get_record_sets
)

st.title("📖 운동 기록 조회")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

history = get_workout_history(user_id)

if not history:
    st.info("저장된 운동 기록이 없습니다.")
    st.stop()

st.write(f"총 {len(history)}개의 운동 세션")

for idx, session in enumerate(history, 1):

    session_id = session.get("session_id")
    workout_date = session.get("workout_date")

    with st.expander(
        f"{idx}. {workout_date} (세션 ID: {session_id})",
        expanded=(idx == 1)
    ):

        workout_records = get_session_workout_records(session_id)

        if not workout_records:
            st.info("운동 기록 없음")
            continue

        total_volume = 0

        for record in workout_records:

            exercise = record.get("exercises", {})
            exercise_name = exercise.get("exercise_name", "운동명 없음")

            st.subheader(exercise_name)

            sets = get_record_sets(
                record["workout_record_id"]
            )

            if not sets:
                st.write("세트 정보 없음")
                continue

            for s in sets:

                weight = s.get("weight", 0)
                reps = s.get("reps", 0)

                volume = float(weight) * int(reps)
                total_volume += volume

                st.write(
                    f"세트 {s['set_number']} | "
                    f"{weight}kg × {reps}회 "
                    f"(볼륨 {volume:.0f})"
                )

            st.divider()

        st.success(
            f"총 운동량: {total_volume:.0f} kg"
        )