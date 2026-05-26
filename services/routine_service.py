from services.supabase_client import supabase


def get_routines():
    response = supabase.table("routines").select("*").execute()
    return response.data