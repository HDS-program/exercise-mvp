"""운동 종목 및 근육 데이터 서비스"""
from services.supabase_client import supabase


def get_all_exercises() -> list:
    """
    모든 운동 종목 조회
    """
    try:
        response = supabase.table("exercises") \
            .select("*") \
            .order("exercise_id") \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 종목 조회 실패: {str(e)}")
        return []


def create_exercise(exercise_name: str, description: str = "") -> dict:
    """
    새 운동 종목 추가
    """
    try:
        data = {
            "exercise_name": exercise_name,
            "description": description
        }

        response = supabase.table("exercises").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        error_message = str(e)

        if "duplicate key value" in error_message or "exercises_exercise_name_key" in error_message:
            return {
                "success": False,
                "data": None,
                "error": "이미 존재하는 운동 종목입니다."
            }

        return {
            "success": False,
            "data": None,
            "error": f"운동 종목 추가 실패: {error_message}"
        }


def get_muscle_groups() -> list:
    """
    모든 근육 부위 조회
    """
    try:
        response = supabase.table("muscle_groups") \
            .select("*") \
            .order("muscle_group_id") \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"근육 부위 조회 실패: {str(e)}")
        return []


def get_exercise_target_muscles(exercise_id: int) -> list:
    """
    운동의 목표 근육 부위 조회
    """
    try:
        response = supabase.table("exercise_target_muscles") \
            .select("muscle_groups(muscle_name)") \
            .eq("exercise_id", exercise_id) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"목표 근육 조회 실패: {str(e)}")
        return []


def search_exercises(search_term: str) -> list:
    """
    운동 종목 검색
    """
    try:
        response = supabase.table("exercises") \
            .select("*") \
            .ilike("exercise_name", f"%{search_term}%") \
            .order("exercise_id") \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 검색 실패: {str(e)}")
        return []


def get_exercises() -> list:
    """
    Workout Input 등 기존 페이지와의 호환용 함수
    """
    return get_all_exercises()