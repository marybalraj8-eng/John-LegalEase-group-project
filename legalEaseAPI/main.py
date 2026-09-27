import sys
import os

# Project root-ஐ path-ல் சேர்க்கிறது
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase API")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "LegalEase API is running on Vercel successfully!"}