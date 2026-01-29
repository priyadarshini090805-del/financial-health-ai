import os
import shutil
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.analysis import (
    load_financials,
    compute_metrics,
    generate_ai_summary,
)

load_dotenv()


app = FastAPI(title="Financial Health AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "uploaded_data"
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_financials(
    income: UploadFile = File(...),
    expenses: UploadFile = File(...),
    loans: UploadFile = File(...)
):
    # Save uploaded files
    income_path = os.path.join(DATA_DIR, income.filename)
    expenses_path = os.path.join(DATA_DIR, expenses.filename)
    loans_path = os.path.join(DATA_DIR, loans.filename)

    with open(income_path, "wb") as f:
        shutil.copyfileobj(income.file, f)

    with open(expenses_path, "wb") as f:
        shutil.copyfileobj(expenses.file, f)

    with open(loans_path, "wb") as f:
        shutil.copyfileobj(loans.file, f)

    # Load data
    income_df, expenses_df, loans_df = load_financials(
        income_path,
        expenses_path,
        loans_path,
    )

    # Compute metrics
    metrics = compute_metrics(income_df, expenses_df, loans_df)

    # Generate AI-style insights
    ai_summary = generate_ai_summary(metrics)

    return {
        "metrics": metrics,
        "ai_summary": ai_summary
    }
