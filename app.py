import streamlit as st

st.set_page_config(
    page_title="Exercise MVP",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ 운동 효율 분석 시스템")

st.write("Streamlit + Supabase MVP 시작")
from services.supabase_client import supabase

response = supabase.table("muscle_groups").select("*").execute()


st.subheader("근육 부위 목록")

for item in response.data:
    st.write(item["muscle_name"])