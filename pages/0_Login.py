import streamlit as st
from services.auth_service import login, signup, logout, get_current_user
from services.user_service import create_user_profile


st.set_page_config(
    page_title="Login - Exercise MVP",
    page_icon="🔐",
    layout="centered"
)


def get_user_email(user_response):
    """
    Supabase get_user() 또는 로그인 결과에서 이메일을 안전하게 꺼내는 함수
    """
    try:
        if hasattr(user_response, "user") and user_response.user:
            return user_response.user.email

        if hasattr(user_response, "email"):
            return user_response.email

        if isinstance(user_response, dict):
            user = user_response.get("user")
            if user and hasattr(user, "email"):
                return user.email

        return "이메일 정보 없음"

    except Exception:
        return "이메일 정보 없음"


st.title("🔐 로그인 / 회원가입")

# 이미 로그인한 경우
current_user_response = get_current_user()

if current_user_response:
    user_email = get_user_email(current_user_response)

    st.success(f"이미 로그인된 상태입니다. ({user_email})")

    if st.button("로그아웃", type="secondary", use_container_width=True):
        logout()
        st.session_state.clear()
        st.success("로그아웃되었습니다.")
        st.rerun()

    st.stop()


# 로그인 / 회원가입 선택
auth_mode = st.radio("선택", ["로그인", "회원가입"], horizontal=True)


if auth_mode == "로그인":
    st.subheader("🔑 로그인")

    email = st.text_input("이메일", placeholder="example@gmail.com")
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력")

    if st.button("로그인", type="primary", use_container_width=True):
        if not email:
            st.warning("이메일을 입력해주세요.")
        elif not password:
            st.warning("비밀번호를 입력해주세요.")
        else:
            with st.spinner("로그인 중..."):
                result = login(email, password)

                if result["success"]:
                    st.session_state.user = result["user"]
                    st.success("✅ 로그인되었습니다!")

                    try:
                        st.switch_page("pages/1_Dashboard.py")
                    except Exception:
                        st.info("왼쪽 메뉴에서 Dashboard를 선택해주세요.")
                else:
                    st.error(f"❌ {result['error']}")


else:
    st.subheader("📝 회원가입")

    col1, col2 = st.columns(2)

    with col1:
        email = st.text_input("이메일", placeholder="example@gmail.com")

    with col2:
        nickname = st.text_input("닉네임", placeholder="사용자 닉네임")

    password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력")
    password_confirm = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호 확인")

    col1, col2 = st.columns(2)

    with col1:
        experience_level = st.selectbox("운동 경험", ["초급", "중급", "상급"])

    with col2:
        goal = st.text_input("운동 목표", placeholder="예: 근력 증진, 다이어트 등")

    if st.button("회원가입", type="primary", use_container_width=True):
        if not email:
            st.warning("이메일을 입력해주세요.")
        elif not nickname:
            st.warning("닉네임을 입력해주세요.")
        elif not password:
            st.warning("비밀번호를 입력해주세요.")
        elif password != password_confirm:
            st.warning("비밀번호가 일치하지 않습니다.")
        else:
            with st.spinner("회원가입 중..."):
                signup_result = signup(email, password)

                if signup_result["success"]:
                    user_id = signup_result["user"].id

                    profile_result = create_user_profile(
                        user_id=user_id,
                        nickname=nickname,
                        experience_level=experience_level,
                        goal=goal
                    )

                    if profile_result["success"]:
                        st.success("✅ 회원가입이 완료되었습니다!")
                        st.info("이제 로그인 탭을 선택하여 로그인하세요.")
                    else:
                        st.warning("회원가입은 완료되었지만 프로필 저장에 실패했습니다.")
                        st.error(f"프로필 생성 실패: {profile_result['error']}")
                else:
                    st.error(f"❌ {signup_result['error']}")


st.divider()
st.info("💡 팁: 회원가입 후 로그인하여 운동 기록을 시작하세요!")