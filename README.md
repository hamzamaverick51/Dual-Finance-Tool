# 💼 Dual Finance Tool — Tax & Installment Planner

> 🔐 Built with FastAPI • 💾 Supabase • ⚙️ Flex API • 🤖 Gemini AI

---

## 🚀 Project Overview

**Dual Finance Tool** is a smart, web-based financial assistant designed to make your money management smarter and simpler.
It provides two essential financial tools:

* 🧾 **Tax Calculator**: Calculates your income tax based on your income, location, and deductions using the powerful **Appexnow Flex API**.
* 📆 **Installment Planner**: Helps you plan how to pay off large expenses in manageable monthly installments.

Integrated with **Supabase** for user authentication and data storage, and enhanced with **Gemini AI** for natural language explanations of financial results.

---

## 🧠 Key Features

* ⚡ **FastAPI Backend**
* 🌐 **Jinja2-Based HTML Templates** (No React/Tailwind)
* 🔐 **User Authentication** via Supabase
* 🧠 **Gemini AI Integration** for financial insight
* 📦 **Appexnow Flex API** for accurate financial calculations
* ☁️ **Ready for AWS Deployment** (Lambda + API Gateway, S3 + CloudFront)

---

## 🗂️ File Structure

```
📁 dual-finance-tool/
├── routes/
│   ├── installment.py
│   ├── reverse.py
│   └── tax.py
├── services/
│   ├── flex_api.py
│   ├── gemini.py
│   ├── supabase_db.py
│   └── __init__.py
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── history.html
│   ├── login.html
│   ├── register.html
│   ├── tax_form.html / tax_result.html
│   ├── installment_form.html / installment_result.html
│   ├── reverse_form.html / reverse_result.html
│   └── error.html
├── auth.py
├── main.py
├── .env
```

---

## 🧩 How It Works

### 🔐 Authentication

* Users can **register and login** using Supabase Auth.
* Session-based authentication allows secure usage of tools.

### 🧾 Tax Calculator

* Users enter income, deductions, and location.
* Calls the **Flex API** to get precise tax data.
* Results are stored in the Supabase `tax_calculations` table.
* Gemini AI explains the results in plain language.

### 📆 Installment Planner

* Users enter total amount, interest rate, and duration.
* Backend calculates monthly payments using **Flex API**.
* Results saved in the `finance_history` table.

### 🔄 Reverse Planner

* Lets users determine how much they can afford monthly.
* Calculates max loan amount from monthly budget.

---

## 🧠 Tech Stack

| Tech              | Role                                     |
| ----------------- | ---------------------------------------- |
| `FastAPI`         | Backend API + Jinja HTML rendering       |
| `Supabase`        | Auth + PostgreSQL Database               |
| `Flex API`        | Tax & installment calculations           |
| `Gemini AI`       | Explanation of complex financial results |
| `Jinja2`          | HTML templates (clean UI)                |
| `AWS Lambda`      | Serverless deployment (planned)          |
| `S3 + CloudFront` | Hosting the frontend HTML files          |

---

## 📸 Screenshots *(Coming Soon)*

> Add visuals like:

* 💻 Homepage
* 🔐 Login/Register
* 📄 Tax form & results
* 📅 Installment planner

---

## 📋 To Do Before Deployment

* [ ] Add Gemini response formatting
* [ ] Finalize Supabase storage integration
* [ ] Connect reverse planner calculations to frontend
* [ ] Host backend on AWS Lambda
* [ ] Upload HTML to AWS S3 + configure CloudFront

---

## 🧑‍💻 Author

👋 Created with passion during an AI/ML internship project.

---

## 🛰️ Deployment (Coming Soon)

* Backend → **AWS Lambda** via API Gateway
* Frontend → **AWS S3 + CloudFront**

---

Let me know if you'd like this saved as a downloadable `README.md` file, or want sections like **API Route Documentation**, **Usage Instructions**, or **Contribution Guidelines** added.
