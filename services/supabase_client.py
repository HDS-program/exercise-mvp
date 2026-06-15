"""Supabase 클라이언트 설정"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

print("SUPABASE_URL =", SUPABASE_URL)
print("SUPABASE_KEY 앞부분 =", SUPABASE_KEY[:20])

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL이 설정되지 않았습니다.")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY가 설정되지 않았습니다.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)