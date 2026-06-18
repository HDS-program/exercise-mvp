"""루틴 관리 서비스"""
from services.supabase_client import supabase


def get_user_routines(user_id: str) -> list:
    """
    사용자의 루틴 목록 조회
    """
    try:
        response = supabase.table("routines") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("routine_id", desc=True) \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"루틴 조회 실패: {str(e)}")
        return []


def get_routine_items(routine_id: int) -> list:
    """
    루틴에 포함된 운동 항목 조회
    """
    try:
        response = supabase.table("routine_items") \
            .select("*, exercises(exercise_name)") \
            .eq("routine_id", routine_id) \
            .order("item_order") \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"루틴 항목 조회 실패: {str(e)}")
        return []


def create_routine(
    user_id: str,
    routine_name: str,
    is_active: bool = True,
    category_id: int | None = None
) -> dict:
    """
    새 루틴 생성
    """
    try:
        data = {
            "user_id": user_id,
            "routine_name": routine_name,
            "is_active": is_active,
            "category_id": category_id
        }

        response = supabase.table("routines").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"루틴 생성 실패: {str(e)}"
        }


def add_routine_item(
    routine_id: int,
    exercise_id: int,
    target_sets: int,
    target_reps: int,
    target_weight: float,
    item_order: int
) -> dict:
    """
    루틴에 운동 항목 추가
    """
    try:
        data = {
            "routine_id": routine_id,
            "exercise_id": exercise_id,
            "target_sets": target_sets,
            "target_reps": target_reps,
            "target_weight": target_weight,
            "item_order": item_order
        }

        response = supabase.table("routine_items").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"루틴 항목 추가 실패: {str(e)}"
        }


def delete_routine(routine_id: int) -> dict:
    """
    루틴 삭제
    """
    try:
        supabase.table("routine_items") \
            .delete() \
            .eq("routine_id", routine_id) \
            .execute()

        supabase.table("routines") \
            .delete() \
            .eq("routine_id", routine_id) \
            .execute()

        return {
            "success": True,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"루틴 삭제 실패: {str(e)}"
        }
def add_exercise_to_routine_by_name(
    routine_id: int,
    exercise_name: str,
    target_sets: int = 3,
    target_reps: int = 10,
    target_weight: float = 0.0
) -> dict:
    """
    운동명으로 루틴에 운동 추가
    """
    try:
        exercise_response = supabase.table("exercises") \
            .select("exercise_id") \
            .eq("exercise_name", exercise_name) \
            .limit(1) \
            .execute()

        if not exercise_response.data:
            return {
                "success": False,
                "data": None,
                "error": f"{exercise_name} 운동을 찾을 수 없습니다."
            }

        exercise_id = exercise_response.data[0]["exercise_id"]

        existing_response = supabase.table("routine_items") \
            .select("*") \
            .eq("routine_id", routine_id) \
            .eq("exercise_id", exercise_id) \
            .execute()

        if existing_response.data:
            return {
                "success": False,
                "data": None,
                "error": f"{exercise_name}은 이미 루틴에 포함되어 있습니다."
            }

        order_response = supabase.table("routine_items") \
            .select("item_order") \
            .eq("routine_id", routine_id) \
            .order("item_order", desc=True) \
            .limit(1) \
            .execute()

        next_order = 1
        if order_response.data:
            next_order = int(order_response.data[0]["item_order"]) + 1

        data = {
            "routine_id": routine_id,
            "exercise_id": exercise_id,
            "target_sets": target_sets,
            "target_reps": target_reps,
            "target_weight": target_weight,
            "item_order": next_order
        }

        response = supabase.table("routine_items").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"추천 운동 루틴 추가 실패: {str(e)}"
        }