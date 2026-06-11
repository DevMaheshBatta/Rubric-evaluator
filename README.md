# 🎓 Rubric-Evaluator

A rubric-based answer evaluation system that uses **FastAPI + LangChain to evaluate student answers against subject-specific rubrics.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Rubric Retrieval** | Keyword matching against 6 subject rubrics + 1 generic fallback |
| **LLM Evaluation** | LangChain + Gemini (gemini-1.5-flash) with structured JSON output |
| **Web UI** | Streamlit with real-time feedback, score bars, criteria breakdown |
| **REST API** | FastAPI with Pydantic schemas and auto-generated docs at `/docs` |
| **CLI** | Coloured terminal interface with interactive mode |
| **Bonus: Comparison** | Side-by-side evaluation with vs. without rubric |

---

## 🏗️ Project Structure

```
Rubric-evaluator/
├── rubrics/
│   ├── rubrics.py            # 6 subject rubrics + generic fallback
│   └── rubric_retriever.py   # Keyword-matching retrieval logic
├── backend/
│   ├── main.py               # FastAPI app with /evaluate, /rubrics endpoints
│   └── evaluator.py          # LangChain chains for with/without rubric eval
├── frontend/
│   └── app.py                # Streamlit web UI
├── cli.py                    # Command-line interface
├── requirements.txt
└── .env.example
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp .env.example .env

# Get it at: https://aistudio.google.com/app/apikey
```

### 3. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4a. Launch the Streamlit UI

```bash
streamlit run frontend/app.py
```

### 4b. Or use the CLI

```bash
# Interactive mode
python cli.py

# Pass arguments directly
python cli.py --question "State Newton's Second Law" --answer "Force equals mass times acceleration"

# With bonus comparison (with vs without rubric)
python cli.py --compare
```

---

## 🎯 How It Works

### Step 1 — Rubric Retrieval

The question text is tokenised (lowercased, punctuation stripped) and scored against each rubric's keyword list using **token overlap counting**:

```python
score = len(question_tokens ∩ rubric_keywords)
```

The rubric with the highest score wins. If all scores are 0, the **generic fallback rubric** is used.

#### Available Rubrics

| Rubric ID | Subject | Level | Keywords (sample) |
|---|---|---|---|
| `physics_class12` | Physics | Class 12 | force, velocity, newton, energy… |
| `mathematics_class12` | Mathematics | Class 12 | integral, derivative, matrix… |
| `english_class10` | English | Class 10 | poem, metaphor, theme, author… |
| `chemistry_class12` | Chemistry | Class 12 | atom, reaction, bond, oxidation… |
| `biology_class12` | Biology | Class 12 | cell, dna, photosynthesis… |
| `history_class10` | History | Class 10 | war, revolution, empire, trade… |
| `generic_fallback` | General | Any | _(no keywords — always fallback)_ |

### Step 2 — LLM-Based Evaluation

LangChain builds a `ChatPromptTemplate` and chains it with `ChatAnthropic` and `StrOutputParser`.

**Prompt (with rubric):**

```
You are a strict but fair academic examiner evaluating a student's answer.
You MUST evaluate ONLY against the provided rubric criteria.
Return ONLY a valid JSON object — no markdown, no preamble.

JSON schema:
{
  "marks_awarded": <int>,
  "max_marks": <int>,
  "feedback": "<actionable feedback>",
  "justification": "<criterion-by-criterion breakdown>",
  "criteria_breakdown": [
    {"criterion": "<name>", "marks_given": <int>, "max": <int>, "comment": "<brief>"}
  ]
}

QUESTION: {question}
STUDENT ANSWER: {student_answer}
RUBRIC — {subject} ({level}): Max marks: {max_marks}
Criteria:
{criteria_text}
```

**Why this prompt works well:**
- "You MUST evaluate ONLY against the provided rubric" — prevents hallucination
- "Return ONLY a valid JSON object" + example schema — forces structured output
- "no markdown, no preamble" — prevents ```json fences from breaking parsing
- `criteria_text` is pre-formatted with marks per criterion — makes allocation unambiguous

### Step 3 — Output

```json
{
  "marks_awarded": 3,
  "max_marks": 5,
  "feedback": "Definition and formula are correct, but the derivation steps are missing.",
  "justification": "1 mark for correct definition, 1 mark for stating F=ma, 0 for missing derivation, 1 for numerical accuracy in worked example, 0 for no diagram.",
  "criteria_breakdown": [
    {"criterion": "Definition / Concept", "marks_given": 1, "max": 1, "comment": "Correct definition stated"},
    {"criterion": "Formula", "marks_given": 1, "max": 1, "comment": "F = ma written"},
    {"criterion": "Derivation / Steps", "marks_given": 0, "max": 1, "comment": "No derivation shown"},
    ...
  ]
}
```

---

## 🔌 API Reference

### `POST /evaluate`

```json
{
  "question": "State Newton's Second Law",
  "student_answer": "Force = mass × acceleration",
  "compare_mode": false
}
```

Response includes `rubric`, `evaluation_with_rubric`, and optionally `evaluation_without_rubric`.

### `GET /rubrics`
Lists all available rubrics.

### `GET /rubrics/{rubric_id}`
Returns a specific rubric with all criteria.

---

## 🔬 Bonus: With vs Without Rubric Comparison

Enable via:
- **Streamlit**: toggle "Compare with/without rubric" in the sidebar
- **CLI**: pass `--compare` flag
- **API**: set `"compare_mode": true`

This runs two LLM calls:
1. Rubric-guided evaluation (controlled, criterion-by-criterion)
2. Free-form evaluation (LLM uses its own judgement)

**Expected finding**: rubric-based evaluation is more consistent, more granular, and provides actionable per-criterion feedback. Without a rubric, scores can vary and feedback is more generic.

---

## 🛠️ Improvements I Would Make

1. **Semantic Retrieval**: Replace keyword matching with embedding-based similarity (e.g. `text-embedding-3-small`) for more accurate rubric selection — especially for question variations that don't use keyword terms directly.

2. **Rubric Management UI**: An admin panel to create, edit, and version rubrics without touching code. Store in a database (PostgreSQL/SQLite) rather than a Python file.

3. **Multi-turn Evaluation**: Let a teacher flag disputes and have the LLM re-evaluate with additional context — a human-in-the-loop re-assessment flow.

4. **Batch Processing**: Accept CSV uploads of question/answer pairs and return bulk evaluation results.

5. **Evaluation Confidence**: Add a `confidence` field to the JSON output so low-confidence evaluations can be flagged for human review.

6. **Caching**: Cache evaluations keyed by `hash(question + answer + rubric_id)` to avoid redundant API calls in classroom settings.

7. **Streaming Responses**: Use streaming API to show evaluation tokens appearing in real-time in the Streamlit UI instead of a loading spinner.

8. **Multilingual Support**: Add Hindi rubrics and enable evaluation of answers written in Hindi or mixed Hindi-English for Indian classroom contexts.

---

## 📦 Tech Stack

- **FastAPI** — REST API backend with Pydantic validation
- **LangChain** — Prompt chaining and LLM abstraction (`langchain-google-genai`)
- **Gemini (gemini-1.5-flash)** — LLM for evaluation via Google AI Studio
- **Streamlit** — Web UI
- **Python 3.11+**
