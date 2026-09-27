import sys
import os

# Project Root Directory-ஐ Python Path-ல் முதன்மையாகச் சேர்க்கிறது
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase API")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "LegalEase API is running successfully!"}