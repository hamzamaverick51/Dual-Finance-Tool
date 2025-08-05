import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from routes import tax, installment, reverse
from auth import register_user, login_user, set_user_session, clear_user_session, get_user_session
from services.supabase_db import get_all_user_history

load_dotenv()

app = FastAPI()

# Set up session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "defaultsecret"))

# Include routers
app.include_router(tax.router)
app.include_router(installment.router)
app.include_router(reverse.router)

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_user_session(request)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_email": user["email"] if user else None})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    result = login_user(email, password)
    if result.get("user"):
        set_user_session(request, email)
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": result.get("error", "Invalid credentials")})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, email: str = Form(...), password: str = Form(...)):
    result = register_user(email, password)
    if result.get("user"):
        set_user_session(request, email)
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request, "error": result.get("error", "Registration failed")})

@app.get("/logout")
async def logout(request: Request):
    clear_user_session(request)
    return RedirectResponse("/", status_code=303)

@app.get("/history", response_class=HTMLResponse)
async def view_history(request: Request):
    user = get_user_session(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    user_email = user["email"]
    all_history = get_all_user_history(user_email)
    # Split by source for template
    tax_history = [h for h in all_history if h["source"] == "tax_calculations"]
    installment_history = [h for h in all_history if h["source"] == "finance_history"]
    reverse_history = [h for h in all_history if h["source"] == "reverse_finance"]
    return templates.TemplateResponse("history.html", {
        "request": request,
        "user_email": user_email,
        "tax_history": tax_history,
        "installment_history": installment_history,
        "reverse_history": reverse_history
    })
