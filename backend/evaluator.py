"""
evaluator.py  —  LangChain + Groq evaluator
"""

import json
import re
import os
import time

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def _get_llm():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not set in .env")
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=key)


WITH_RUBRIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an examiner. Evaluate the answer using ONLY the rubric. Return JSON only: {{\"marks_awarded\":int,\"max_marks\":int,\"feedback\":\"str\",\"justification\":\"str\",\"criteria_breakdown\":[{{\"criterion\":\"str\",\"marks_given\":int,\"max\":int,\"comment\":\"str\"}}]}}"),
    ("human", "Q: {question}\n\nAnswer: {student_answer}\n\nRubric ({subject}, {level}, max {max_marks} marks):\n{criteria_text}"),
])

WITHOUT_RUBRIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an examiner. Grade this answer out of 5. Return JSON only: {{\"marks_awarded\":int,\"max_marks\":5,\"feedback\":\"str\",\"justification\":\"str\"}}"),
    ("human", "Q: {question}\n\nAnswer: {student_answer}"),
])


def _format_criteria(criteria: list[dict]) -> str:
    return "\n".join(
        f"{i}. [{c['max_marks']}mk] {c['name']}: {c['description']}"
        for i, c in enumerate(criteria, 1)
    )


def _parse_json_response(raw: str) -> dict:
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    # Extract the first complete JSON object, ignoring any trailing text
    decoder = json.JSONDecoder()
    try:
        result, _ = decoder.raw_decode(raw)
        return result
    except json.JSONDecodeError:
        # Fallback: find outermost { } block and parse that
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError(f"No JSON object found in response:\n{raw}")
        return json.loads(raw[start:end])


def _call_with_retry(chain, inputs: dict) -> str:
    raw = None
    for attempt in range(3):
        try:
            raw = chain.invoke(inputs)
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() and attempt < 2:
                print(f"Rate limit hit. Waiting 15s... (attempt {attempt + 1}/3)")
                time.sleep(15)
            else:
                raise
    if raw is None:
        raise RuntimeError("All 3 retry attempts failed.")
    return raw


def evaluate_with_rubric(question: str, student_answer: str, rubric: dict) -> dict:
    chain = WITH_RUBRIC_PROMPT | _get_llm() | StrOutputParser()
    raw = _call_with_retry(chain, {
        "question": question,
        "student_answer": student_answer,
        "subject": rubric["subject"],
        "level": rubric["level"],
        "max_marks": rubric["max_marks"],
        "criteria_text": _format_criteria(rubric["criteria"]),
    })
    result = _parse_json_response(raw)
    result["rubric_used"] = rubric["id"]
    result["subject"] = rubric["subject"]
    return result


def evaluate_without_rubric(question: str, student_answer: str) -> dict:
    chain = WITHOUT_RUBRIC_PROMPT | _get_llm() | StrOutputParser()
    raw = _call_with_retry(chain, {"question": question, "student_answer": student_answer})
    result = _parse_json_response(raw)
    result["rubric_used"] = "none"
    result["subject"] = "Unknown"
    return result