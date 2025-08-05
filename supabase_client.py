from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file (important for local dev)
load_dotenv()

# Fetch Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create a Supabase client instance
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
