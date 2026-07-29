
import os
from supabase import create_client, Client
from app.config import SUPABASE_SERVICE_ROLE_KEY,SUPABASE_URL

_client: Client = None

def get_db() -> Client:
    global _client
    if _client is None:
        _client = create_client(
            SUPABASE_URL,
            SUPABASE_SERVICE_ROLE_KEY
        )
    return _client