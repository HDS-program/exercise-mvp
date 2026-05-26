from services.supabase_client import supabase


def get_workout_sessions():
    response = supabase.table("workout_sessions").select("*").execute()
    return response.data