import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.agents.crew import ResearchCrew
from src.services.rag import ensure_dirs
from src.utils.config import settings

ensure_dirs()

app = FastAPI(
    title="CrewAI Multi-Agent Research Pipeline",
    version="1.0.0",
    description="CrewAI + Gemini + Tavily + ChromaDB + FastAPI on AWS Lambda",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "crewai-research-pipeline"}


@app.post("/research")
def research(
    topic: str = Form(...),
    use_web_search: bool = Form(True),
):
    """Run multi-agent research (no PDF)."""
    try:
        report = ResearchCrew(topic=topic, use_web_search=use_web_search).run()
        return {"topic": topic, "report": report, "pdfs_ingested": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research/with-pdf")
def research_with_pdf(
    topic: str = Form(...),
    use_web_search: bool = Form(True),
    files: list[UploadFile] = File(default=[]),
):
    """Run multi-agent research with optional PDF uploads."""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for file in files:
        if file.filename and file.filename.lower().endswith(".pdf"):
            safe_name = f"{uuid.uuid4().hex[:8]}_{file.filename}"
            dest = upload_dir / safe_name
            with open(dest, "wb") as f:
                shutil.copyfileobj(file.file, f)
            saved_paths.append(str(dest))

    try:
        report = ResearchCrew(
            topic=topic,
            use_web_search=use_web_search,
            pdf_paths=saved_paths,
        ).run()
        return {"topic": topic, "report": report, "pdfs_ingested": len(saved_paths)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# AWS Lambda entry point
handler = Mangum(app)
