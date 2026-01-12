# app/main.py

from fastapi import FastAPI, Request, HTTPException
import json
from pathlib import Path

app = FastAPI()

PROJECT_FILE = Path(__file__).parent / "projects.json"

def load_projects():
    with open(PROJECT_FILE) as f:
        return json.load(f)

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
