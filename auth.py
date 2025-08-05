from fastapi import Request
from typing import Optional
from services.supabase_db import supabase  # Supabase client import

# ---------------------- AUTH FUNCTIONS ----------------------

def register_user(email: str, password: str) -> dict:
    """
    Registers a new user with Supabase Auth.
    Returns a dict with keys: 'session', 'user', or 'error'.
    """
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return {"user": response.user, "session": response.session}
    except Exception as e:
        return {"error": str(e)}

def login_user(email: str, password: str) -> dict:
    """
    Logs in a user with Supabase Auth using email and password.
    Returns a dict with keys: 'session', 'user', or 'error'.
    """
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"user": response.user, "session": response.session}
    except Exception as e:
        return {"error": str(e)}

# ---------------------- SESSION HELPERS ----------------------

def set_user_session(request: Request, email: str):
    """
    Saves the user's email in the session.
    """
    request.session["user_email"] = email

def clear_user_session(request: Request):
    """
    Clears the current session.
    """
    request.session.clear()

def get_user_session(request: Request) -> Optional[dict]:
    """
    Returns a user-like dict if email exists in session.
    """
    email = request.session.get("user_email")
    if email:
        return {"email": email}
    return None
