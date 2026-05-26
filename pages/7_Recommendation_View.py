import streamlit as st
from services.recommendation_service import get_recommendations

st.title("추천 조회")

recommendations = get_recommendations()

st.write(recommendations)