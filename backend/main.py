from fastapi import FastAPI

app = FastAPI(title="Financial Health AI")

@app.get("/")
def health_check():
    return {"status": "ok"}
