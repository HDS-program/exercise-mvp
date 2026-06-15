"""회복 기록 서비스"""
from services.supabase_client import supabase


def check_recovery_exists(session_id: int) -> bool:
    """
    세션에 대한 회복 기록이 이미 존재하는지 확인
    """
    try:
        response = supabase.table("recovery_records") \
            .select("*") \
            .eq("session_id", session_id) \
            .execute()

        return len(response.data) > 0

    except Exception:
        return False


def get_sessions_without_recovery(user_id: str) -> list:
    """
    회복 기록이 없는 최근 운동 세션 조회
    """
    try:
        all_sessions = supabase.table("workout_sessions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .execute()

        if not all_sessions.data:
            return []

        sessions_without_recovery = []

        for session in all_sessions.data:
            session_id = session.get("session_id")

            if session_id is None:
                continue

            if not check_recovery_exists(session_id):
                sessions_without_recovery.append(session)

        return sessions_without_recovery

    except Exception as e:
        print(f"회복 필요 세션 조회 실패: {str(e)}")
        return []


def create_recovery_record(
    session_id: int,
    recovery_date: str,
    overall_fatigue: int,
    overall_condition: int,
    memo: str = ""
) -> dict:
    """
    전체 회복 기록 생성
    """
    try:
        data = {
    "session_id": session_id,
    "recorded_date": recovery_date,
    "overall_fatigue": overall_fatigue,
    "overall_condition": overall_condition,
    "memo": memo
}

        response = supabase.table("recovery_records").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"회복 기록 생성 실패: {str(e)}"
        }


def create_muscle_recovery_record(
    recovery_id: int,
    muscle_id: int,
    soreness: int,
    pain: int,
    recovery_status: int
) -> dict:
    """
    부위별 회복 기록 생성
    """
    try:
        data = {
            "recovery_id": recovery_id,
            "muscle_id": muscle_id,
            "soreness": soreness,
            "pain": pain,
            "recovery_status": recovery_status
        }

        response = supabase.table("recovery_muscle_records").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"근육 회복 기록 생성 실패: {str(e)}"
        }


def get_latest_recovery_record(user_id: str) -> dict | None:
    """
    사용자의 최신 회복 기록 조회
    """
    try:
        sessions = supabase.table("workout_sessions") \
            .select("session_id") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .limit(1) \
            .execute()

        if not sessions.data:
            return None

        latest_session_id = sessions.data[0]["session_id"]

        response = supabase.table("recovery_records") \
            .select("*") \
            .eq("session_id", latest_session_id) \
            .execute()

        return response.data[0] if response.data else None

    except Exception as e:
        print(f"최신 회복 기록 조회 실패: {str(e)}")
        return None


def get_muscle_recovery_records(recovery_id: int) -> list:
    """
    회복 기록의 부위별 회복 데이터 조회
    """
    try:
        response = supabase.table("recovery_muscle_records") \
            .select("*, muscle_groups(muscle_name)") \
            .eq("recovery_id", recovery_id) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"부위별 회복 기록 조회 실패: {str(e)}")
        return []