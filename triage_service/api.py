from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from database import TriageDatabase

app = FastAPI()
db = None

@app.get("/cases")
def get_cases(page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100)):
    offset = (page - 1) * page_size
    cases, total = db.get_cases(limit=page_size, offset=offset)
    return {
        "cases": cases,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@app.get("/cases/{case_id}")
def get_case(case_id: str):
    case = db.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@app.get("/cases/priority/{priority}")
def get_cases_by_priority(priority: int):
    return db.get_cases_by_priority(priority)
