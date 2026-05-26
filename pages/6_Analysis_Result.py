import streamlit as st
from services.analysis_service import get_analysis_results

st.title("분석 결과 조회")

analysis_results = get_analysis_results()

st.write(analysis_results)