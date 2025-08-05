import json
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.gemini import gemini_summary
from services.flex_api import get_installment_plan
from services.supabase_db import save_finance_history
from auth import get_user_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/installments", response_class=HTMLResponse)
def get_installment_form(request: Request):
    return templates.TemplateResponse("installment_form.html", {"request": request})

@router.post("/installments", response_class=HTMLResponse)
def calculate_installment(
    request: Request,
    amount: float = Form(...),
    rate: float = Form(...),
    tenure: int = Form(...)
):
    try:
        # Get user session
        user = get_user_session(request)
        if not user:
            return RedirectResponse("/login", status_code=303)
        user_email = user["email"]

        # Call Flex API
        plan = get_installment_plan({"amount": amount, "interest": rate, "tenure": tenure})
        if not plan:
            raise Exception("Installment plan API failed.")
        emi = float(plan.get("emi", 0.0) or 0.0)
        installments = plan.get("installments", [])
        result = [
            {
                "month": item.get("month"),
                "principal": f"{item.get('principal', 0.0):.2f}",
                "interest": f"{item.get('interest', 0.0):.2f}",
                "remaining_balance": f"{item.get('balance', 0.0):.2f}"
            }
            for item in installments
        ]
        result_json = json.dumps({
            "monthly_payment": emi,
            "installments": result
        }, indent=4)

        # Gemini summary
        summary_prompt = (
            f"The user has taken a loan of {amount} at an interest rate of {rate}% for {tenure} months. "
            f"The monthly EMI is {emi:.2f}. Explain this in simple, beginner-friendly terms."
        )
        summary = gemini_summary(summary_prompt) or "(AI summary unavailable)"

        # Save to Supabase (finance_history table)
        save_finance_history(
            email=user_email,
            calculation_type="Installment",
            tax_year=0,  # Not relevant for installment
            income=amount,
            calculated_tax=emi
        )

        return templates.TemplateResponse("installment_result.html", {
            "request": request,
            "result": result,
            "result_json": result_json,
            "emi": f"{emi:.2f}",
            "summary": summary
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Something went wrong during the EMI calculation: {str(e)}"
        })
