import streamlit as st
from services.exercise_service import get_exercises

st.title("운동 기록 입력")

exercise_list = get_exercises()

exercise_names = [exercise["exercise_name"] for exercise in exercise_list]

selected_exercise = st.selectbox(
    "운동 선택",
    exercise_names
)

weight = st.number_input("중량", min_value=0)
reps = st.number_input("반복 횟수", min_value=0)

if st.button("운동 기록 저장"):
    st.success("운동 기록 저장 완료")