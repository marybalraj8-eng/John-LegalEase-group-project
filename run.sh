#!/usr/bin/env bash
echo "Starting FastAPI Backend..."
uvicorn legalEaseAPI.main:app --reload --port 8000 &

echo "Starting Streamlit Frontend..."
streamlit run frontend/app.py