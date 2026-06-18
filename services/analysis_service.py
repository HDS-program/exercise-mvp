"""분석 및 추천 서비스"""
from services.supabase_client import supabase


def get_latest_workout_session(user_id: str) -> dict | None:
    """
    사용자의 최신 운동 세션 조회
    """
    try:
        response = supabase.table("workout_sessions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("workout_date", desc=True) \
            .order("session_id", desc=True) \
            .limit(1) \
            .execute()

        return response.data[0] if response.data else None

    except Exception as e:
        print(f"최신 운동 세션 조회 실패: {str(e)}")
        return None


def get_latest_recovery_for_user(user_id: str) -> dict | None:
    """
    사용자의 최신 회복 기록 조회
    """
    try:
        latest_session = get_latest_workout_session(user_id)

        if not latest_session:
            return None

        session_id = latest_session["session_id"]

        response = supabase.table("recovery_records") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("recorded_date", desc=True) \
            .limit(1) \
            .execute()

        return response.data[0] if response.data else None

    except Exception as e:
        print(f"최신 회복 기록 조회 실패: {str(e)}")
        return None


def get_latest_workout_records(session_id: int) -> list:
    """
    특정 운동 세션의 운동 기록 조회
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


def get_workout_sets(workout_record_id: int) -> list:
    """
    운동 기록의 세트 정보 조회
    """
    try:
        response = supabase.table("workout_sets") \
            .select("*") \
            .eq("workout_record_id", workout_record_id) \
            .order("set_number") \
            .execute()

        return response.data if response.data else []

    except Exception as e:
        print(f"운동 세트 조회 실패: {str(e)}")
        return []


def get_simple_analysis(user_id: str) -> dict | None:
    """
    운동 기록과 회복 기록을 기반으로 즉석 분석 결과 생성
    """
    try:
        session = get_latest_workout_session(user_id)

        if not session:
            return None

        session_id = session["session_id"]
        workout_date = session.get("workout_date")

        workout_records = get_latest_workout_records(session_id)
        recovery = get_latest_recovery_for_user(user_id)

        total_volume = 0
        exercise_names = []
        exercise_ids = []

        for record in workout_records:
            workout_record_id = record.get("workout_record_id")
            exercise_id = record.get("exercise_id")
            exercise_data = record.get("exercises")

            if exercise_id is not None:
                exercise_ids.append(exercise_id)

            if isinstance(exercise_data, dict):
                exercise_names.append(exercise_data.get("exercise_name", "운동명 없음"))

            sets = get_workout_sets(workout_record_id)

            for s in sets:
                weight = s.get("weight") or 0
                reps = s.get("reps") or 0
                total_volume += float(weight) * int(reps)

        fatigue = recovery.get("overall_fatigue") if recovery else None
        condition = recovery.get("overall_condition") if recovery else None

        if recovery:
            if fatigue >= 8 or condition <= 3:
                status = "회복 부족"
                message = "피로도가 높거나 컨디션이 낮습니다. 오늘은 휴식 또는 가벼운 회복 운동을 추천합니다."
            elif fatigue >= 6 or condition <= 5:
                status = "주의 필요"
                message = "회복 상태가 완전하지 않습니다. 최근 사용한 근육 부위는 피하고 다른 부위 위주로 가볍게 운동하는 것이 좋습니다."
            else:
                status = "회복 양호"
                message = "회복 상태가 양호합니다. 최근 사용한 부위를 고려하여 다음 운동을 진행할 수 있습니다."
        else:
            status = "회복 기록 없음"
            message = "아직 해당 운동에 대한 회복 기록이 없습니다. 회복 기록을 입력하면 더 정확한 분석이 가능합니다."

        return {
            "session_id": session_id,
            "workout_date": workout_date,
            "exercise_ids": exercise_ids,
            "exercise_names": exercise_names,
            "total_volume": total_volume,
            "recovery": recovery,
            "fatigue": fatigue,
            "condition": condition,
            "status": status,
            "message": message
        }

    except Exception as e:
        print(f"간단 분석 생성 실패: {str(e)}")
        return None


def get_latest_analysis_result(user_id: str) -> dict | None:
    """
    기존 화면 호환용 함수
    """
    return get_simple_analysis(user_id)


def get_analysis_history(user_id: str, limit: int = 10) -> list:
    """
    최근 운동 세션 목록 조회
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
        print(f"분석 이력 조회 실패: {str(e)}")
        return []


def get_target_muscle_ids_by_exercise_ids(exercise_ids: list) -> list:
    """
    최근 수행한 운동들이 사용하는 근육 ID 조회
    """
    try:
        if not exercise_ids:
            return []

        response = supabase.table("exercise_target_muscles") \
            .select("muscle_group_id") \
            .in_("exercise_id", exercise_ids) \
            .execute()

        if not response.data:
            return []

        muscle_ids = []

        for row in response.data:
            muscle_id = row.get("muscle_group_id")
            if muscle_id is not None and muscle_id not in muscle_ids:
                muscle_ids.append(muscle_id)

        return muscle_ids

    except Exception as e:
        print(f"최근 사용 근육 조회 실패: {str(e)}")
        return []


def get_muscle_names_by_ids(muscle_ids: list) -> list:
    """
    근육 ID 목록을 근육 이름 목록으로 변환
    """
    try:
        if not muscle_ids:
            return []

        response = supabase.table("muscle_groups") \
            .select("muscle_group_id, muscle_name") \
            .in_("muscle_group_id", muscle_ids) \
            .execute()

        if not response.data:
            return []

        return [row.get("muscle_name") for row in response.data if row.get("muscle_name")]

    except Exception as e:
        print(f"근육 이름 조회 실패: {str(e)}")
        return []


def get_exercises_excluding_muscles(excluded_muscle_ids: list, limit: int = 3) -> list:
    """
    최근 사용한 근육을 제외하고 추천 가능한 운동 조회
    """
    try:
        all_exercises_response = supabase.table("exercises") \
            .select("exercise_id, exercise_name") \
            .order("exercise_id") \
            .execute()

        if not all_exercises_response.data:
            return []

        all_exercises = all_exercises_response.data

        if not excluded_muscle_ids:
            return [e.get("exercise_name") for e in all_exercises[:limit]]

        target_response = supabase.table("exercise_target_muscles") \
            .select("exercise_id, muscle_group_id") \
            .execute()

        blocked_exercise_ids = set()

        for row in target_response.data or []:
            if row.get("muscle_group_id") in excluded_muscle_ids:
                blocked_exercise_ids.add(row.get("exercise_id"))

        recommended = []

        for exercise in all_exercises:
            exercise_id = exercise.get("exercise_id")
            exercise_name = exercise.get("exercise_name")

            if exercise_id not in blocked_exercise_ids and exercise_name:
                recommended.append(exercise_name)

            if len(recommended) >= limit:
                break

        if recommended:
            return recommended

        return [e.get("exercise_name") for e in all_exercises[:limit] if e.get("exercise_name")]

    except Exception as e:
        print(f"부위 제외 추천 운동 조회 실패: {str(e)}")
        return []


def get_low_intensity_exercises_excluding_muscles(excluded_muscle_ids: list, limit: int = 3) -> list:
    """
    회복 부족/주의 상태에서 사용할 가벼운 운동 추천
    """
    try:
        preferred_names = [
            "페이스풀",
            "레그익스텐션",
            "레그컬",
            "플랭크",
            "사이드레터럴레이즈",
            "케이블 푸쉬다운",
            "바벨컬"
        ]

        all_exercises_response = supabase.table("exercises") \
            .select("exercise_id, exercise_name") \
            .in_("exercise_name", preferred_names) \
            .execute()

        if not all_exercises_response.data:
            return get_exercises_excluding_muscles(excluded_muscle_ids, limit)

        target_response = supabase.table("exercise_target_muscles") \
            .select("exercise_id, muscle_group_id") \
            .execute()

        blocked_exercise_ids = set()

        for row in target_response.data or []:
            if row.get("muscle_group_id") in excluded_muscle_ids:
                blocked_exercise_ids.add(row.get("exercise_id"))

        recommended = []

        for exercise in all_exercises_response.data:
            exercise_id = exercise.get("exercise_id")
            exercise_name = exercise.get("exercise_name")

            if exercise_id not in blocked_exercise_ids and exercise_name:
                recommended.append(exercise_name)

            if len(recommended) >= limit:
                break

        if recommended:
            return recommended

        return get_exercises_excluding_muscles(excluded_muscle_ids, limit)

    except Exception as e:
        print(f"저강도 추천 운동 조회 실패: {str(e)}")
        return get_exercises_excluding_muscles(excluded_muscle_ids, limit)


def get_latest_recommendation(user_id: str) -> dict | None:
    """
    최신 분석 기반 추천 생성
    """
    analysis = get_simple_analysis(user_id)

    if not analysis:
        return None

    fatigue = analysis.get("fatigue")
    condition = analysis.get("condition")
    recent_exercise_ids = analysis.get("exercise_ids", [])

    used_muscle_ids = get_target_muscle_ids_by_exercise_ids(recent_exercise_ids)
    used_muscle_names = get_muscle_names_by_ids(used_muscle_ids)

    if fatigue is None or condition is None:
        return {
            "title": "회복 기록 입력 필요",
            "recommendation": "먼저 Recovery Input에서 회복 기록을 입력해주세요.",
            "intensity": "판단 불가",
            "recommended_exercises": [],
            "used_muscles": used_muscle_names,
            "reason": "회복 기록이 없어 운동 추천을 계산할 수 없습니다."
        }

    if fatigue >= 8 or condition <= 3:
        recommended_exercises = get_low_intensity_exercises_excluding_muscles(
            used_muscle_ids,
            limit=3
        )

        return {
            "title": "휴식 추천",
            "recommendation": "피로도가 높거나 컨디션이 낮으므로 고강도 운동은 피하고, 최근 사용한 근육 부위는 제외한 가벼운 회복 운동을 추천합니다.",
            "intensity": "낮음",
            "recommended_exercises": recommended_exercises,
            "used_muscles": used_muscle_names,
            "reason": "최근 운동에서 사용한 근육 부위를 제외하고 부상 위험이 낮은 운동을 우선 추천했습니다."
        }

    if fatigue >= 6 or condition <= 5:
        recommended_exercises = get_low_intensity_exercises_excluding_muscles(
            used_muscle_ids,
            limit=3
        )

        return {
            "title": "가벼운 운동 추천",
            "recommendation": "회복이 완전하지 않으므로 최근 사용한 근육은 피하고, 중량과 세트 수를 낮춰 진행하는 것이 좋습니다.",
            "intensity": "중간 이하",
            "recommended_exercises": recommended_exercises,
            "used_muscles": used_muscle_names,
            "reason": "피로도와 컨디션이 중간 수준이므로 최근 사용한 근육 부위를 제외하고 비교적 부담이 낮은 운동을 추천했습니다."
        }

    recommended_exercises = get_exercises_excluding_muscles(
        used_muscle_ids,
        limit=3
    )

    return {
        "title": "정상 운동 가능",
        "recommendation": "회복 상태가 양호하므로 최근 사용한 근육 부위를 제외하고 다른 부위 운동을 진행해도 좋습니다.",
        "intensity": "보통",
        "recommended_exercises": recommended_exercises,
        "used_muscles": used_muscle_names,
        "reason": "최근 운동에서 사용한 근육 부위를 고려하여 겹치지 않는 운동을 추천했습니다."
    }


def get_recommendations_list(user_id: str, limit: int = 5) -> list:
    """
    추천 목록 호환용
    """
    recommendation = get_latest_recommendation(user_id)

    if not recommendation:
        return []

    return [recommendation]


def save_recommendation_action(
    user_id: str,
    action_type: str,
    action_score: int,
    recommendation_id: int | None = None
) -> dict:
    """
    추천 수락/거절 기록 저장
    """
    try:
        data = {
            "recommendation_id": recommendation_id,
            "user_id": user_id,
            "action_type": action_type,
            "action_score": action_score
        }

        response = supabase.table("recommendation_actions").insert(data).execute()

        return {
            "success": True,
            "data": response.data[0] if response.data else None,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"추천 행동 저장 실패: {str(e)}"
        }