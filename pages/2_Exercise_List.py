import streamlit as st
from services.exercise_service import get_exercises

st.title("운동 목록")

exercise_list = get_exercises()

for exercise in exercise_list:
    st.write(exercise["exercise_name"])