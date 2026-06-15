"""분석 및 추천 서비스"""
from services.supabase_client import supabase

def get_latest_analysis_result(user_id: str) -> dict:
    """
    사용자의 최신 분석 결과 조회
    
    Args:
        user_id: 사용자 ID
    
    Returns:
        최신 분석 결과
    """
    try:
        # 사용자의 가장 최신 운동 세션 ID 조회
        session_response = supabase.table("workout_sessions")\
            .select("id")\
            .eq("user_id", user_id)\
            .order("workout_date", desc=True)\
            .limit(1)\
            .execute()
        
        if not session_response.data:
            return None
        
        session_id = session_response.data[0]['id']
        
        # 해당 세션의 분석 결과 조회
        response = supabase.table("analysis_results")\
            .select("*")\
            .eq("session_id", session_id)\
            .execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"분석 결과 조회 실패: {str(e)}")
        return None

def get_analysis_history(user_id: str, limit: int = 10) -> list:
    """
    사용자의 분석 결과 이력 조회
    
    Args:
        user_id: 사용자 ID
        limit: 조회 개수
    
    Returns:
        분석 결과 이력
    """
    try:
        # 사용자의 모든 운동 세션 ID 조회
        sessions_response = supabase.table("workout_sessions")\
            .select("id")\
            .eq("user_id", user_id)\
            .order("workout_date", desc=True)\
            .limit(limit)\
            .execute()
        
        if not sessions_response.data:
            return []
        
        session_ids = [session['id'] for session in sessions_response.data]
        
        # 각 세션의 분석 결과 조회
        response = supabase.table("analysis_results")\
            .select("*")\
            .in_("session_id", session_ids)\
            .order("created_at", desc=True)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"분석 이력 조회 실패: {str(e)}")
        return []

def get_latest_recommendation(user_id: str) -> dict:
    """
    사용자의 최신 추천 결과 조회
    
    Args:
        user_id: 사용자 ID
    
    Returns:
        최신 추천 결과
    """
    try:
        # 최신 분석 결과 조회
        analysis = get_latest_analysis_result(user_id)
        if not analysis:
            return None
        
        # 해당 분석 결과의 추천 조회
        response = supabase.table("recommendations")\
            .select("*, exercises(exercise_name), muscle_groups(muscle_name)")\
            .eq("analysis_id", analysis['id'])\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"추천 결과 조회 실패: {str(e)}")
        return None

def get_recommendations_list(user_id: str, limit: int = 5) -> list:
    """
    사용자의 추천 결과 목록 조회
    
    Args:
        user_id: 사용자 ID
        limit: 조회 개수
    
    Returns:
        추천 결과 목록
    """
    try:
        # 사용자의 모든 분석 결과 조회
        analysis_response = supabase.table("analysis_results")\
            .select("id")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        if not analysis_response.data:
            return []
        
        analysis_ids = [a['id'] for a in analysis_response.data]
        
        # 각 분석 결과의 추천 조회
        response = supabase.table("recommendations")\
            .select("*, exercises(exercise_name), muscle_groups(muscle_name)")\
            .in_("analysis_id", analysis_ids)\
            .order("created_at", desc=True)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"추천 목록 조회 실패: {str(e)}")
        return []
