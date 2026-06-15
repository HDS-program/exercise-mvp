import streamlit as st
from services.auth_service import logout

st.set_page_config(
    page_title="Settings - Exercise MVP",
    page_icon="⚙️",
    layout="centered"
)

st.title("⚙️ 설정")

if st.button("🔴 로그아웃", type="secondary", use_container_width=True):
    result = logout()
    if result['success']:
        st.success("로그아웃되었습니다.")
        st.session_state.clear()
        st.switch_page("pages/0_Login.py")
    else:
        st.error(f"로그아웃 실패: {result['error']}")
