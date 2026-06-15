"""루틴 관리 서비스"""
from services.supabase_client import supabase

def get_user_routines(user_id: str) -> list:
    """
    사용자의 루틴 목록 조회
    
    Args:
        user_id: 사용자 ID
    
    Returns:
        루틴 목록
    """
    try:
        response = supabase.table("routines")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"루틴 조회 실패: {str(e)}")
        return []

def get_routine_items(routine_id: int) -> list:
    """
    루틴에 포함된 운동 항목 조회
    
    Args:
        routine_id: 루틴 ID
    
    Returns:
        루틴 항목 목록
    """
    try:
        response = supabase.table("routine_items")\
            .select("*, exercises(exercise_name)")\
            .eq("routine_id", routine_id)\
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"루틴 항목 조회 실패: {str(e)}")
        return []

def create_routine(user_id: str, routine_name: str, is_active: bool = True) -> dict:
    """
    새 루틴 생성
    
    Args:
        user_id: 사용자 ID
        routine_name: 루틴명
        is_active: 활성화 여부
    
    Returns:
        {'success': bool, 'data': dict or None, 'error': str or None}
    """
    try:
        data = {
            "user_id": user_id,
            "routine_name": routine_name,
            "is_active": is_active
        }
        response = supabase.table("routines").insert(data).execute()
        return {
            'success': True,
            'data': response.data[0] if response.data else None,
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': f'루틴 생성 실패: {str(e)}'
        }

def add_routine_item(routine_id: int, exercise_id: int, target_sets: int, target_reps: int, target_weight: float) -> dict:
    """
    루틴에 운동 항목 추가
    
    Args:
        routine_id: 루틴 ID
        exercise_id: 운동 ID
        target_sets: 목표 세트 수
        target_reps: 목표 반복 횟수
        target_weight: 목표 중량
    
    Returns:
        {'success': bool, 'data': dict or None, 'error': str or None}
    """
    try:
        data = {
            "routine_id": routine_id,
            "exercise_id": exercise_id,
            "target_sets": target_sets,
            "target_reps": target_reps,
            "target_weight": target_weight
        }
        response = supabase.table("routine_items").insert(data).execute()
        return {
            'success': True,
            'data': response.data[0] if response.data else None,
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': f'루틴 항목 추가 실패: {str(e)}'
        }
