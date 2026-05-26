import streamlit as st
from services.routine_service import get_routines

st.title("루틴 조회")

routine_list = get_routines()

st.write(routine_list)