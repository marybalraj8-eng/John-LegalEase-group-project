from fastapi import FastAPI
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase API")

app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "LegalEase API is running live on Vercel!"}