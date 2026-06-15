"""인증 서비스"""

from services.supabase_client import supabase


def login(email: str, password: str) -> dict:
    """
    이메일과 비밀번호로 로그인
    """
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )

        if response.user:
            return {
                "success": True,
                "user": response.user,
                "error": None
            }

        return {
            "success": False,
            "user": None,
            "error": "로그인에 실패했습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "user": None,
            "error": f"로그인 중 오류가 발생했습니다: {str(e)}"
        }


def logout() -> dict:
    """
    로그아웃
    """
    try:
        supabase.auth.sign_out()
        return {
            "success": True,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_current_user():
    """
    현재 로그인된 사용자 객체만 반환한다.
    Supabase get_user()는 UserResponse를 반환하므로,
    실제 사용자 정보는 response.user 안에 있다.
    """
    try:
        response = supabase.auth.get_user()

        if response and response.user:
            return response.user

        return None

    except Exception:
        return None


def signup(email: str, password: str) -> dict:
    """
    회원가입
    """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if response.user:
            return {
                "success": True,
                "user": response.user,
                "error": None
            }

        return {
            "success": False,
            "user": None,
            "error": "회원가입에 실패했습니다."
        }

    except Exception as e:
        return {
            "success": False,
            "user": None,
            "error": f"회원가입 중 오류가 발생했습니다: {str(e)}"
        }