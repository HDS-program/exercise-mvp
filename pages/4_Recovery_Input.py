import streamlit as st
from datetime import datetime

from services.auth_service import get_current_user
from services.recovery_service import (
    get_sessions_without_recovery,
    create_recovery_record,
    create_muscle_recovery_record
)
from services.exercise_service import get_muscle_groups


st.title("🩹 회복 기록 입력")

user = get_current_user()

if not user:
    st.warning("로그인이 필요합니다. 먼저 로그인해주세요.")
    st.stop()

user_id = user.id

try:
    st.subheader("1️⃣ 회복 기록 대상 운동 선택")

    sessions_without_recovery = get_sessions_without_recovery(user_id)

    if not sessions_without_recovery:
        st.info("회복 기록을 입력할 운동 기록이 없습니다.")
        st.stop()

    session_options = {}

    for session in sessions_without_recovery:
        workout_date = session.get("workout_date", "날짜 없음")
        session_id = session.get("session_id")
        routine_id = session.get("routine_id")

        routine_data = session.get("routines")

        if isinstance(routine_data, dict):
            routine_name = routine_data.get("routine_name", "루틴 없음")
        else:
            routine_name = "루틴 없음"

        if routine_id is None:
            routine_name = "루틴 없음"

        label = f"{workout_date} - {routine_name} (세션:{session_id})"
        session_options[label] = session_id

    selected_session_label = st.selectbox(
        "운동 선택",
        list(session_options.keys())
    )

    selected_session_id = session_options[selected_session_label]

    st.subheader("2️⃣ 회복 상태 기록")

    recovery_date = st.date_input("회복 기록 날짜", datetime.now())

    col1, col2 = st.columns(2)

    with col1:
        overall_fatigue = st.slider("전체 피로도 (1-10)", 1, 10, 5)

    with col2:
        overall_condition = st.slider("전체 컨디션 (1-10)", 1, 10, 5)

    st.subheader("3️⃣ 부위별 회복 상태")

    muscle_groups = get_muscle_groups()

    if not muscle_groups:
        st.warning("근육 부위 데이터를 불러올 수 없습니다. 전체 회복 기록만 저장할 수 있습니다.")
        muscle_recovery_data = {}
    else:
        muscle_recovery_data = {}

        for muscle in muscle_groups:
            muscle_id = muscle.get("muscle_group_id")
            muscle_name = muscle.get("muscle_name", "Unknown")

            if muscle_id is None:
                continue

            st.write(f"**{muscle_name}**")

            col1, col2, col3 = st.columns(3)

            with col1:
                soreness = st.slider(
                    f"{muscle_name} 근육통 (0-10)",
                    0,
                    10,
                    3,
                    key=f"soreness_{muscle_id}"
                )

            with col2:
                pain = st.slider(
                    f"{muscle_name} 통증 (0-10)",
                    0,
                    10,
                    0,
                    key=f"pain_{muscle_id}"
                )

            with col3:
                recovery_status = st.slider(
                    f"{muscle_name} 회복 정도 (0-10)",
                    0,
                    10,
                    5,
                    key=f"recovery_{muscle_id}"
                )

            muscle_recovery_data[muscle_id] = {
                "soreness": soreness,
                "pain": pain,
                "recovery_status": recovery_status
            }

            st.divider()

    st.subheader("4️⃣ 메모")

    memo = st.text_area("회복 상태에 대한 메모 (선택사항)", "")

    if st.button("회복 기록 저장", type="primary"):
        recovery_result = create_recovery_record(
            session_id=selected_session_id,
            recovery_date=str(recovery_date),
            overall_fatigue=overall_fatigue,
            overall_condition=overall_condition,
            memo=memo
        )

        if not recovery_result["success"]:
            st.error(f"회복 기록 생성 실패: {recovery_result['error']}")
            st.stop()

        recovery_id = recovery_result["data"]["recovery_id"]

        for muscle_id, data in muscle_recovery_data.items():
            muscle_result = create_muscle_recovery_record(
                recovery_id=recovery_id,
                muscle_id=muscle_id,
                soreness=data["soreness"],
                pain=data["pain"],
                recovery_status=data["recovery_status"]
            )

            if not muscle_result["success"]:
                st.warning(f"부위별 회복 기록 저장 실패: {muscle_result['error']}")

        st.success("✅ 회복 기록이 저장되었습니다!")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")