from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

import os

TRIAGE_SERVICE_URL = os.getenv('TRIAGE_SERVICE_URL', 'http://localhost:8000')

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html") as f:
        return f.read()

@app.get("/api/cases")
async def get_cases():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRIAGE_SERVICE_URL}/cases")
        data = response.json()
        data["cases"] = sorted(data["cases"], key=lambda x: x["priority"])
        return data
