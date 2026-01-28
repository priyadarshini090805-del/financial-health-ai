import pandas as pd

def load_financials(income_path, expenses_path, loans_path):
    income = pd.read_csv(income_path)
    expenses = pd.read_csv(expenses_path)
    loans = pd.read_csv(loans_path)
    return income, expenses, loans


def compute_metrics(income, expenses, loans):
    total_income = income["amount"].sum()
    total_expenses = expenses["amount"].sum()

    monthly_income = total_income
    monthly_expenses = total_expenses

    operating_profit = total_income - total_expenses
    net_margin = operating_profit / total_income if total_income > 0 else 0

    total_emi = loans["monthly_emi"].sum() if not loans.empty else 0
    debt_service_ratio = total_emi / monthly_income if monthly_income > 0 else 0

    cash_runway_months = (
        operating_profit / monthly_expenses if monthly_expenses > 0 else 0
    )

    metrics = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "operating_profit": operating_profit,
        "net_margin": round(net_margin, 2),
        "monthly_emi": total_emi,
        "debt_service_ratio": round(debt_service_ratio, 2),
        "cash_runway_months": round(cash_runway_months, 2),
    }

    return metrics
