import streamlit as st
from services.recovery_service import get_muscle_groups

st.title("회복 기록 입력")

muscle_groups = get_muscle_groups()

muscle_names = [muscle["muscle_name"] for muscle in muscle_groups]

selected_muscle = st.selectbox(
    "근육 부위 선택",
    muscle_names
)

recovery_score = st.slider(
    "회복 상태",
    1,
    10
)

if st.button("회복 기록 저장"):
    st.success("회복 기록 저장 완료")