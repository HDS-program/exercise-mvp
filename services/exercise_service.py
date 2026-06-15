"""운동 종목 및 근육 데이터 서비스"""
from services.supabase_client import supabase


def get_all_exercises() -> list:
    """
    모든 운동 종목 조회

    Returns:
        운동 종목 목록
    """
    try:
        response = supabase.table("exercises").select("*").execute()
        return response.data if response.data else []

    except Exception as e:
        print(f"운동 종목 조회 실패: {str(e)}")
        return []


def get_muscle_groups() -> list:
    """
    모든 근육 부위 조회

    Returns:
        근육 부위 목록
    """
    try:
        response = supabase.table("muscle_groups").select("*").execute()
        return response.data if response.data else []

    except Exception as e:
        print(f"근육 부위 조회 실패: {str(e)}")
        return []


def get_exercise_target_muscles(exercise_id: int) -> list:
    """
    운동의 목표 근육 부위 조회

    Args:
        exercise_id: 운동 ID

    Returns:
        목표 근육 부위 목록
    """
    try:
        response = (
            supabase.table("exercise_target_muscles")
            .select("muscle_groups(muscle_name)")
            .eq("exercise_id", exercise_id)
            .execute()
        )

        return response.data if response.data else []

    except Exception as e:
        print(f"목표 근육 조회 실패: {str(e)}")
        return []


def search_exercises(search_term: str) -> list:
    """
    운동 종목 검색

    Args:
        search_term: 검색어

    Returns:
        검색 결과 목록
    """
    try:
        response = (
            supabase.table("exercises")
            .select("*")
            .ilike("exercise_name", f"%{search_term}%")
            .execute()
        )

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 검색 실패: {str(e)}")
        return []


def get_exercises() -> list:
    """
    기존 페이지(Workout_Input 등)와의 호환성을 위한 함수.
    모든 운동 종목을 반환한다.

    Returns:
        운동 종목 목록
    """
    return get_all_exercises()