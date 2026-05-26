from services.supabase_client import supabase


def get_muscle_groups():
    response = supabase.table("muscle_groups").select("*").execute()
    return response.data