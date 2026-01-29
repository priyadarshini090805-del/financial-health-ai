import pandas as pd


def load_financials(income_path, expenses_path, loans_path):
    income = pd.read_csv(income_path)
    expenses = pd.read_csv(expenses_path)
    loans = pd.read_csv(loans_path)
    return income, expenses, loans


def compute_metrics(income, expenses, loans):
    total_income = float(income["amount"].sum())
    total_expenses = float(expenses["amount"].sum())

    operating_profit = total_income - total_expenses
    net_margin = operating_profit / total_income if total_income > 0 else 0.0

    total_emi = float(loans["monthly_emi"].sum()) if not loans.empty else 0.0
    debt_service_ratio = total_emi / total_income if total_income > 0 else 0.0

    cash_runway_months = (
        operating_profit / total_expenses if total_expenses > 0 else 0.0
    )

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "operating_profit": round(operating_profit, 2),
        "net_margin": round(net_margin, 2),
        "monthly_emi": round(total_emi, 2),
        "debt_service_ratio": round(debt_service_ratio, 2),
        "cash_runway_months": round(cash_runway_months, 2),
    }


def generate_ai_summary(metrics: dict):
    score = 100
    risks = []
    advice = []

    if metrics["net_margin"] < 0.1:
        score -= 25
        risks.append("Low profit margin")
        advice.append("Reduce unnecessary expenses and review pricing.")

    if metrics["debt_service_ratio"] > 0.4:
        score -= 25
        risks.append("High debt burden")
        advice.append("Restructure loans or increase monthly revenue.")

    if metrics["cash_runway_months"] < 1:
        score -= 25
        risks.append("Cash flow stress")
        advice.append("Improve receivables collection and control cash burn.")

    score = max(score, 0)

    if not advice:
        advice.append("Financial health looks stable. Maintain discipline.")

    return {
        "health_score": score,
        "risks": risks,
        "advice": " ".join(advice)
    }
