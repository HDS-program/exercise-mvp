from services.supabase_client import supabase


def get_analysis_results():
    response = supabase.table("analysis_results").select("*").execute()
    return response.data