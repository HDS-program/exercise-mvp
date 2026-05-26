from services.supabase_client import supabase


def get_users():
    response = supabase.table("user_profiles").select("*").execute()
    return response.data