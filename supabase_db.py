import os
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------- SAVE FUNCTIONS ----------------------

def save_finance_history(email: str, calculation_type: str, tax_year: int, income: float, calculated_tax: float):
    data = {
        "user_email": email,
        "created_at": datetime.utcnow().isoformat(),
        "calculation_type": calculation_type,
        "tax_year": tax_year,
        "income": income,
        "calculated_tax": calculated_tax
    }
    response = supabase.table("finance_history").insert(data).execute()
    return response.data


def save_reverse_finance(email: str, interest_rate: float, results, total_amount: float, duration: int):
    data = {
        "user_email": email,
        "created_at": datetime.utcnow().isoformat(),
        "interest_rate": interest_rate,
        "results": results,  # Can be dict (will be stored as JSON) or str
        "total_amount": total_amount,
        "duration": duration
    }
    response = supabase.table("reverse_finance").insert(data).execute()
    return response.data


def save_tax_calculation(email: str, income: float, location: str, deductions: float, result):
    data = {
        "user_email": email,
        "created_at": datetime.utcnow().isoformat(),
        "income": income,
        "location": location,
        "deductions": deductions,
        "result": result
    }
    response = supabase.table("tax_calculations").insert(data).execute()
    return response.data

# ---------------------- FETCH FUNCTIONS ----------------------

def get_finance_history(email: str):
    response = supabase.table("finance_history").select("*").eq("user_email", email).order("created_at", desc=True).execute()
    return response.data

def get_reverse_finance(email: str):
    response = supabase.table("reverse_finance").select("*").eq("user_email", email).order("created_at", desc=True).execute()
    return response.data

def get_tax_calculations(email: str):
    response = supabase.table("tax_calculations").select("*").eq("user_email", email).order("created_at", desc=True).execute()
    return response.data

def get_all_user_history(email: str):
    """Fetches all user history from all three tables, sorted by created_at desc."""
    finance = get_finance_history(email)
    reverse = get_reverse_finance(email)
    tax = get_tax_calculations(email)
    # Add a 'source' field to each for display
    for row in finance:
        row['source'] = 'finance_history'
    for row in reverse:
        row['source'] = 'reverse_finance'
    for row in tax:
        row['source'] = 'tax_calculations'
    all_rows = finance + reverse + tax
    # Sort by created_at desc
    all_rows.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return all_rows
