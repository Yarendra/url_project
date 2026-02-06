# app/main.py

from fastapi import FastAPI, Request, HTTPException
from functools import lru_cache
import json
from pathlib import Path

app = FastAPI()

PROJECT_FILE = Path(__file__).parent / "projects.json"

@lru_cache
def load_projects():
    try:
        with open(PROJECT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid projects.json: {e}"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="projects.json not found"
        )

@app.get("/endpoint/{project_id}")
async def resolve_project(project_id: str):
    projects = load_projects()

    project = projects.get(project_id)

    if not project:
        raise HTTPException(404, "Unknown project")

    return {
        "project_id": project_id,
        "target_url": project["url"]
    }
