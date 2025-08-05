from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json

from services.flex_api import get_installment_plan  # Not used here, but for consistency
from services.gemini import gemini_summary
from services.supabase_db import save_tax_calculation
from auth import get_user_session

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/tax", response_class=HTMLResponse)
def get_tax_form(request: Request):
    return templates.TemplateResponse("tax_form.html", {"request": request})

@router.post("/tax", response_class=HTMLResponse)
def post_tax_form(
    request: Request,
    income: float = Form(...),
    location: str = Form(...),
    deductions: float = Form(0.0)
):
    try:
        user = get_user_session(request)
        if not user:
            return RedirectResponse("/login", status_code=303)
        user_email = user["email"]

        # Call Flex API (simulate tax calculation)
        # Replace with actual tax calculation API call if available
        # For now, let's simulate a result
        calculated_tax = income * 0.15  # Example: 15% flat tax
        tax_result = {
            "income": income,
            "location": location,
            "deductions": deductions,
            "calculated_tax": calculated_tax
        }
        result_json = json.dumps(tax_result, indent=4)

        # Gemini summary
        summary_prompt = (
            f"The user has an income of {income} from {location} with deductions of {deductions}. "
            f"The calculated tax is {calculated_tax}. Please explain it in simple terms."
        )
        summary = gemini_summary(summary_prompt) or "(AI summary unavailable)"

        # Save to Supabase (tax_calculations table)
        save_tax_calculation(
            email=user_email,
            income=income,
            location=location,
            deductions=deductions,
            result=calculated_tax
        )

        return templates.TemplateResponse("tax_result.html", {
            "request": request,
            "result_json": result_json,
            "summary": summary
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Tax calculation failed: {e}"
        })
