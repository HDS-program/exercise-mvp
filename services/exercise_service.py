from services.supabase_client import supabase


def get_exercises():
    response = supabase.table("exercises").select("*").execute()
    return response.data