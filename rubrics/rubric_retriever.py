"""
rubric_retriever.py
-------------------
Retrieves the most relevant rubric for a given question using keyword matching.
No embeddings required — pure token overlap scoring.
"""

import re
from typing import Optional
from rubrics.rubrics import RUBRICS


def _tokenize(text: str) -> set[str]:
    """Lowercase, strip punctuation, split into word tokens."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return set(text.split())


def retrieve_rubric(question: str) -> dict:
    """
    Return the rubric whose keywords overlap most with the question tokens.
    Falls back to the generic rubric when no subject-specific match is found.

    Scoring logic:
      score = number of keyword tokens that appear in the question
    The fallback rubric (empty keywords list) always scores 0 and is only
    selected when every subject-specific rubric also scores 0.
    """
    question_tokens = _tokenize(question)

    best_score = 0
    best_rubric: Optional[dict] = None

    subject_rubrics = [r for r in RUBRICS if r["id"] != "generic_fallback"]
    fallback = next(r for r in RUBRICS if r["id"] == "generic_fallback")

    for rubric in subject_rubrics:
        keyword_tokens = _tokenize(" ".join(rubric["keywords"]))
        score = len(question_tokens & keyword_tokens)
        if score > best_score:
            best_score = score
            best_rubric = rubric

    # Return subject rubric only if we got at least one keyword hit
    if best_rubric and best_score > 0:
        return {**best_rubric, "_match_score": best_score, "_matched_by": "keyword"}

    return {**fallback, "_match_score": 0, "_matched_by": "fallback"}
