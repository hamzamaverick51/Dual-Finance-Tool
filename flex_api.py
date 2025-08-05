import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional
from datetime import datetime

# Load .env variables
load_dotenv()

BASE_URL = os.getenv("FLEX_API_BASE_URL")  # e.g. https://stage-api-k8s.netsolapp.io
FLEX_API_KEY = os.getenv("FLEX_API_KEY")
FLEX_API_VERSION = os.getenv("FLEX_API_VERSION", "1.0")  # Default to 1.0 if not set

if not BASE_URL or not FLEX_API_KEY:
    raise EnvironmentError("Missing FLEX_API_BASE_URL or FLEX_API_KEY in .env")

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": FLEX_API_KEY,
    "x-api-version": FLEX_API_VERSION
}

# Installment Planner API Call (RentalAmountAnnuity)
def get_installment_plan(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        url = f"{BASE_URL}/calculate/RentalAmountAnnuity"
        payload = {
            "requestParam": {
                "apr": data.get("interest"),
                "contractTerms": data.get("tenure"),
                "rentalMode": "Arrear",
                "residualValue": 0,
                "rentalFrequency": "Monthly",
                "financedAmount": data.get("amount"),
                "productRateConversionMethod": "Simple"
            },
            "startDate": datetime.utcnow().isoformat() + "Z",
            "extensionDays": 0
        }
        print("[FlexAPI] URL:", url)
        print("[FlexAPI] Headers:", HEADERS)
        print("[FlexAPI] Payload:", payload)
        response = requests.post(url, headers=HEADERS, json=payload)
        print("[FlexAPI] Status Code:", response.status_code)
        print("[FlexAPI] Response Text:", response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[FlexAPI Error] Installment Plan failed: {e}")
        return None

# Reverse Finance Planner API Call (ReverseFinanceAmount)
def get_reverse_finance(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        url = f"{BASE_URL}/calculate/ReverseFinanceAmount"
        payload = {
            "requestParam": {
                "monthlyRental": data.get("monthly_budget"),
                "apr": data.get("interest"),
                "contractTerms": data.get("tenure"),
                "rentalMode": "Arrear",
                "residualValue": 0,
                "rentalFrequency": "Monthly",
                "productRateConversionMethod": "Simple"
            },
            "startDate": datetime.utcnow().isoformat() + "Z",
            "extensionDays": 0
        }
        print("[FlexAPI] URL:", url)
        print("[FlexAPI] Headers:", HEADERS)
        print("[FlexAPI] Payload:", payload)
        response = requests.post(url, headers=HEADERS, json=payload)
        print("[FlexAPI] Status Code:", response.status_code)
        print("[FlexAPI] Response Text:", response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[FlexAPI Error] Reverse Finance failed: {e}")
        return None
