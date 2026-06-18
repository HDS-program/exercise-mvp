import streamlit as st

from services.exercise_service import (
    get_all_exercises,
    create_exercise
)


st.title("💪 운동 종목 조회")

st.subheader("➕ 새 운동 종목 추가")

with st.form("add_exercise_form"):
    exercise_name = st.text_input("운동명", placeholder="예: 데드리프트")
    description = st.text_area("운동 설명", placeholder="예: 등과 하체를 함께 사용하는 복합 운동")

    submitted = st.form_submit_button("운동 종목 추가", type="primary")

    if submitted:
        if not exercise_name.strip():
            st.warning("운동명을 입력해주세요.")
        else:
            result = create_exercise(
                exercise_name=exercise_name.strip(),
                description=description.strip()
            )

            if result["success"]:
                st.success("✅ 운동 종목이 추가되었습니다.")
                st.rerun()
            else:
                st.error(result["error"])

st.divider()

try:
    exercises = get_all_exercises()

    st.subheader(f"총 {len(exercises)}개의 운동 종목")

    search_term = st.text_input("운동 검색", "")

    if search_term:
        exercises = [
            e for e in exercises
            if search_term.lower() in e.get("exercise_name", "").lower()
        ]

    if exercises:
        for exercise in exercises:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.write(f"**{exercise.get('exercise_name', 'N/A')}**")
                    st.caption(exercise.get("description", "설명 없음"))

                with col2:
                    st.write(f"ID: {exercise.get('exercise_id', 'N/A')}")
    else:
        st.info("검색 결과가 없습니다.")

except Exception as e:
    st.error(f"운동 목록을 불러오는 중 오류가 발생했습니다: {str(e)}")