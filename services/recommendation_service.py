from services.supabase_client import supabase


def get_recommendations():
    response = supabase.table("recommendations").select("*").execute()
    return response.data