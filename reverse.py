from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.flex_api import get_reverse_finance
from services.gemini import gemini_summary
from services.supabase_db import save_reverse_finance
from auth import get_user_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/reverse", response_class=HTMLResponse)
def get_reverse_form(request: Request):
    return templates.TemplateResponse("reverse_form.html", {"request": request})

@router.post("/reverse", response_class=HTMLResponse)
def post_reverse_form(
    request: Request,
    monthly_budget: float = Form(...),
    interest: float = Form(...),
    tenure: int = Form(...)
):
    try:
        user = get_user_session(request)
        if not user:
            return RedirectResponse("/login", status_code=303)
        user_email = user["email"]

        # Call Flex API
        result = get_reverse_finance({
            "monthly_budget": monthly_budget,
            "interest": interest,
            "tenure": tenure
        })
        if not result:
            raise Exception("Reverse finance API failed.")
        eligible_loan = result.get("eligible_loan", 0.0)

        # Gemini summary
        prompt = (
            f"A user can pay Rs {monthly_budget} per month at an interest of {interest}% for {tenure} months. "
            f"Help them understand their loan eligibility of Rs {eligible_loan:.2f} in simple terms."
        )
        summary = gemini_summary(prompt) or "(AI summary unavailable)"

        # Save to Supabase
        save_reverse_finance(
            email=user_email,
            interest_rate=interest,
            results=result,
            total_amount=eligible_loan,
            duration=tenure
        )

        return templates.TemplateResponse("reverse_result.html", {
            "request": request,
            "result": {
                "monthly_budget": monthly_budget,
                "interest": interest,
                "tenure": tenure,
                "eligible_loan": eligible_loan
            },
            "summary": summary
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Reverse EMI calculation failed: {e}"
        })
