"""사용자 정보 서비스"""
from services.supabase_client import supabase

def get_user_profile(user_id: str) -> dict:
    """
    사용자 프로필 조회
    
    Args:
        user_id: 사용자 ID
    
    Returns:
        사용자 프로필 데이터 또는 None
    """
    try:
        response = supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"사용자 프로필 조회 실패: {str(e)}")
        return None

def create_user_profile(user_id: str, nickname: str, experience_level: str = "초급", goal: str = "") -> dict:
    """
    사용자 프로필 생성
    
    Args:
        user_id: 사용자 ID
        nickname: 닉네임
        experience_level: 운동 경력 수준
        goal: 운동 목표
    
    Returns:
        {'success': bool, 'data': dict or None, 'error': str or None}
    """
    try:
        data = {
            "user_id": user_id,
            "nickname": nickname,
            "experience_level": experience_level,
            "goal": goal
        }
        response = supabase.table("user_profiles").insert(data).execute()
        return {
            'success': True,
            'data': response.data[0] if response.data else None,
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': f'프로필 생성 실패: {str(e)}'
        }

def update_user_profile(user_id: str, **kwargs) -> dict:
    """
    사용자 프로필 수정
    
    Args:
        user_id: 사용자 ID
        **kwargs: 수정할 필드들
    
    Returns:
        {'success': bool, 'data': dict or None, 'error': str or None}
    """
    try:
        response = supabase.table("user_profiles").update(kwargs).eq("user_id", user_id).execute()
        return {
            'success': True,
            'data': response.data[0] if response.data else None,
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': f'프로필 수정 실패: {str(e)}'
        }
