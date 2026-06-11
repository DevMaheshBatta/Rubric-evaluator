"""
evaluator.py  —  LangChain + Gemini evaluator
"""

import json
import re
import os
import time
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def _get_llm() -> ChatGoogleGenerativeAI:
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY is not set. Add it to your .env file.")
    return ChatGoogleGenerativeAI(
        # Updated from gemini-1.5-flash to gemini-2.0-flash to resolve 404 error
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=key,
    )


WITH_RUBRIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a strict but fair academic examiner evaluating a student's answer.
You MUST evaluate ONLY against the provided rubric criteria.
Return ONLY a valid JSON object — no markdown, no preamble, no explanation outside the JSON.

JSON schema:
{{
  "marks_awarded": <integer>,
  "max_marks": <integer>,
  "feedback": "<one or two sentences of actionable feedback for the student>",
  "justification": "<criterion-by-criterion breakdown explaining marks given or deducted>",
  "criteria_breakdown": [
    {{"criterion": "<name>", "marks_given": <int>, "max": <int>, "comment": "<brief comment>"}}
  ]
}}"""),
    ("human", """QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

RUBRIC — {subject} ({level}):
Max marks: {max_marks}

Criteria:
{criteria_text}

Evaluate the student's answer strictly according to the rubric above and return the JSON."""),
])

WITHOUT_RUBRIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a strict but fair academic examiner evaluating a student's answer WITHOUT a specific rubric.
Use your general knowledge to assess the quality of the answer on a 5-mark scale.
Return ONLY a valid JSON object — no markdown, no preamble, no explanation outside the JSON.

JSON schema:
{{
  "marks_awarded": <integer 0-5>,
  "max_marks": 5,
  "feedback": "<one or two sentences of actionable feedback>",
  "justification": "<explain why these marks were awarded based on content quality, accuracy, and completeness>"
}}"""),
    ("human", """QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

Evaluate the answer and return the JSON."""),
])


def _format_criteria(criteria: list[dict]) -> str:
    lines = []
    for i, c in enumerate(criteria, 1):
        lines.append(
            f"{i}. [{c['max_marks']} mark{'s' if c['max_marks'] > 1 else ''}] "
            f"{c['name']}: {c['description']}"
        )
    return "\n".join(lines)


def _parse_json_response(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw.strip())



def evaluate_with_rubric(question: str, student_answer: str, rubric: dict) -> dict:
    llm = _get_llm()
    chain = WITH_RUBRIC_PROMPT | llm | StrOutputParser()
    
    # Try up to 3 times if rate limited
    for attempt in range(3):
        try:
            raw = chain.invoke({
                "question": question,
                "student_answer": student_answer,
                "subject": rubric["subject"],
                "level": rubric["level"],
                "max_marks": rubric["max_marks"],
                "criteria_text": _format_criteria(rubric["criteria"]),
            })
            break  # Success! Break out of the loop
        except ChatGoogleGenerativeAIError as e:
            if "RESOURCE_EXHAUSTED" in str(e) and attempt < 2:
                print("Rate limit hit. Waiting 45 seconds to retry...")
                time.sleep(45)  # Wait for the window to reset
                continue
            raise e  # If it fails on the last try or is a different error, raise it
            
    result = _parse_json_response(raw)
    result["rubric_used"] = rubric["id"]
    result["subject"] = rubric["subject"]
    return result


def evaluate_without_rubric(question: str, student_answer: str) -> dict:
    llm = _get_llm()
    chain = WITHOUT_RUBRIC_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({"question": question, "student_answer": student_answer})
    result = _parse_json_response(raw)
    result["rubric_used"] = "none"
    result["subject"] = "Unknown"
    return result
