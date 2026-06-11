"""
main.py  —  FastAPI backend for Rubric-Evaluator
"""

import sys
import os
import traceback

# Load .env file FIRST before anything else
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rubrics.rubric_retriever import retrieve_rubric
from backend.evaluator import evaluate_with_rubric, evaluate_without_rubric

# ── Startup check ─────────────────────────────────────────────────────────────

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("⚠️  WARNING: GOOGLE_API_KEY is not set! Evaluation calls will fail.")
    print("   Create a .env file with: GOOGLE_API_KEY=AIza...")
else:
    print(f"✅ GOOGLE_API_KEY loaded (starts with: {api_key[:8]}...)")

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Rubric-Evaluator API",
    description="Rubric-based answer evaluation using LangChain + Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────────────────────────

class EvaluateRequest(BaseModel):
    question: str = Field(..., min_length=5)
    student_answer: str = Field(..., min_length=1)
    compare_mode: bool = Field(False)


class CriterionBreakdown(BaseModel):
    criterion: str
    marks_given: int
    max: int
    comment: str


class EvaluationResult(BaseModel):
    marks_awarded: int
    max_marks: int
    feedback: str
    justification: str
    rubric_used: str
    subject: str
    criteria_breakdown: list[CriterionBreakdown] = []


class RubricInfo(BaseModel):
    id: str
    subject: str
    level: str
    max_marks: int
    match_score: int
    matched_by: str
    criteria: list[dict]


class EvaluateResponse(BaseModel):
    rubric: RubricInfo
    evaluation_with_rubric: EvaluationResult
    evaluation_without_rubric: EvaluationResult | None = None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "Mini Answer Evaluator",
        "google_api_key_set": bool(os.getenv("GOOGLE_API_KEY")),
    }


@app.post("/evaluate", response_model=EvaluateResponse, tags=["Evaluation"])
def evaluate(request: EvaluateRequest):
    try:
        # Step 1: Rubric retrieval
        rubric = retrieve_rubric(request.question)

        # Step 2: LLM evaluation with rubric
        result_with = evaluate_with_rubric(
            request.question, request.student_answer, rubric
        )

        # Step 3 (optional): evaluation without rubric
        result_without = None
        if request.compare_mode:
            result_without = evaluate_without_rubric(
                request.question, request.student_answer
            )

        return EvaluateResponse(
            rubric=RubricInfo(
                id=rubric["id"],
                subject=rubric["subject"],
                level=rubric["level"],
                max_marks=rubric["max_marks"],
                match_score=rubric.get("_match_score", 0),
                matched_by=rubric.get("_matched_by", "unknown"),
                criteria=rubric["criteria"],
            ),
            evaluation_with_rubric=EvaluationResult(**result_with),
            evaluation_without_rubric=(
                EvaluationResult(**result_without) if result_without else None
            ),
        )

    except Exception as e:
        # Print full traceback to server console so you can see what went wrong
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rubrics", tags=["Rubrics"])
def list_rubrics():
    from rubrics.rubrics import RUBRICS
    return [
        {
            "id": r["id"],
            "subject": r["subject"],
            "level": r["level"],
            "max_marks": r["max_marks"],
            "criteria_count": len(r["criteria"]),
        }
        for r in RUBRICS
    ]


@app.get("/rubrics/{rubric_id}", tags=["Rubrics"])
def get_rubric(rubric_id: str):
    from rubrics.rubrics import RUBRICS
    rubric = next((r for r in RUBRICS if r["id"] == rubric_id), None)
    if not rubric:
        raise HTTPException(status_code=404, detail=f"Rubric '{rubric_id}' not found")
    return rubric
