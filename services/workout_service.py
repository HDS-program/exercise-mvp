"""운동 기록 서비스"""
from services.supabase_client import supabase


def create_workout_session(user_id: str, routine_id: int | None, workout_date: str) -> dict:
    """
    운동 세션 생성
    """
    try:
        data = {
            "user_id": user_id,
            "routine_id": routine_id,
            "workout_date": workout_date
        }

        response = supabase.table("workout_sessions").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"운동 세션 생성 실패: {str(e)}"
        }


def create_workout_record(session_id: int, exercise_id: int) -> dict:
    """
    운동 기록 생성
    """
    try:
        data = {
            "session_id": session_id,
            "exercise_id": exercise_id
        }

        response = supabase.table("workout_records").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"운동 기록 생성 실패: {str(e)}"
        }


def create_workout_set(record_id: int, set_number: int, weight: float, reps: int) -> dict:
    """
    운동 세트 기록 생성
    """
    try:
        data = {
            "workout_record_id": record_id,
            "set_number": set_number,
            "weight": weight,
            "reps": reps
        }

        response = supabase.table("workout_sets").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"운동 세트 생성 실패: {str(e)}"
        }


def record_stimulus_muscles(record_id: int, muscle_id: int, stimulus_intensity: int) -> dict:
    """
    운동 직후 자극 부위 기록
    """
    try:
        data = {
            "workout_record_id": record_id,
            "muscle_id": muscle_id,
            "stimulus_intensity": stimulus_intensity
        }

        response = supabase.table("workout_record_muscles").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"자극 부위 기록 실패: {str(e)}"
        }


def get_user_recent_workouts(user_id: str, limit: int = 5) -> list:
    """
    사용자의 최근 운동 세션 조회
    """
    try:
        response = supabase.table("workout_sessions") \
            .select("*, routines(routine_name)") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .limit(limit) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"최근 운동 조회 실패: {str(e)}")
        return []


def get_session_details(session_id: int) -> dict | None:
    """
    운동 세션 상세 조회
    """
    try:
        response = supabase.table("workout_sessions") \
            .select("*") \
            .eq("session_id", session_id) \
            .execute()

        return response.data[0] if response.data else None

    except Exception as e:
        print(f"세션 조회 실패: {str(e)}")
        return None
    
def get_workout_history(user_id: str, limit: int = 20) -> list:
    """
    운동 기록 조회
    """

    try:
        response = supabase.table("workout_sessions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .order("session_id", desc=True) \
            .limit(limit) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 기록 조회 실패: {str(e)}")
        return []

def get_workout_history(user_id: str, limit: int = 20) -> list:
    """
    사용자의 운동 세션 목록 조회
    """

    try:
        response = supabase.table("workout_sessions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .order("session_id", desc=True) \
            .limit(limit) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 이력 조회 실패: {str(e)}")
        return []


def get_session_workout_records(session_id: int) -> list:
    """
    특정 세션 운동 목록 조회
    """

    try:
        response = supabase.table("workout_records") \
            .select("*, exercises(exercise_name)") \
            .eq("session_id", session_id) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 기록 조회 실패: {str(e)}")
        return []


def get_record_sets(workout_record_id: int) -> list:
    """
    특정 운동 세트 조회
    """

    try:
        response = supabase.table("workout_sets") \
            .select("*") \
            .eq("workout_record_id", workout_record_id) \
            .order("set_number") \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"세트 조회 실패: {str(e)}")
        return []