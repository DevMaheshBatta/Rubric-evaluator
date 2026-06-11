# 🎯 Rubic-Evaluator

**AI-Powered Rubric-Grounded Answer Evaluation System**

Rubic-Evaluator is an intelligent assessment platform that evaluates student answers using predefined grading rubrics and Google Gemini. By grounding evaluations in subject-specific rubrics, the system delivers fair, transparent, and explainable grading instead of relying solely on generic LLM judgments.

---

## 📸 Application Preview

![Rubic-Evaluator UI](screenshots/app-preview.png)

The application enables users to:

* Enter a question
* Submit a student answer
* Retrieve the most relevant rubric
* Generate AI-powered evaluation
* View marks, feedback, and justification
* Compare evaluation with and without rubric grounding

---

## 🚀 Features

* ✅ Rubric-Based Answer Evaluation
* ✅ Google Gemini Integration
* ✅ LangChain-Powered Prompting
* ✅ FastAPI Backend
* ✅ Streamlit Interactive UI
* ✅ Keyword-Based Rubric Retrieval
* ✅ Subject-Specific Rubrics
* ✅ Fallback Generic Rubric
* ✅ Structured JSON Output
* ✅ Detailed Feedback & Justification
* ✅ Compare With/Without Rubric Evaluation

---

## 🧠 Problem Statement

Large Language Models can evaluate answers, but they often:

* Produce inconsistent marks
* Lack grading transparency
* Ignore subject-specific marking schemes
* Provide vague explanations

Rubic-Evaluator addresses these limitations by first retrieving a relevant grading rubric and then evaluating the answer against explicit criteria.

---

## 💡 Solution

```text
Question
    ↓
Rubric Retrieval
    ↓
Relevant Rubric
    ↓
Gemini Evaluation
    ↓
Marks + Feedback + Justification
```

This ensures evaluations are:

* Fair
* Explainable
* Consistent
* Aligned with academic grading standards

---

## 🏗️ Architecture

```text
┌──────────────────────────┐
│      Streamlit UI        │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│       FastAPI API        │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│    Rubric Retriever      │
│   (Keyword Matching)     │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│   Retrieved Rubric       │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ LangChain Prompt Engine  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│     Google Gemini        │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Structured JSON Output   │
└──────────────────────────┘
```
📂 Project Structure
Rubric-evaluator/
│
├── backend/
│   ├── main.py
│   ├── evaluator.py
│   └── __init__.py
│
├── frontend/
│   └── app.py
│
├── rubrics/
│   ├── rubrics.py
│   ├── rubric_retriever.py
│   └── __init__.py
│
├── .env.example
├── requirements.txt
└── README.md
```
---

## 🔍 Rubric Retrieval

The system uses keyword matching to identify the most relevant rubric.

### Example

**Question**

```text
State Newton's Second Law of Motion and derive F = ma.
```

**Retrieved Rubric**

```text
Physics → Derivation Rubric
```

If no suitable rubric is found, the system automatically switches to a generic fallback rubric.

---

## 📚 Supported Rubrics

| Subject     | Evaluation Type               |
| ----------- | ----------------------------- |
| Physics     | Definitions, Derivations      |
| Mathematics | Methods, Steps, Final Answer  |
| English     | Explanation, Clarity, Grammar |
| Generic     | Fallback Evaluation           |

---

## 🤖 LLM Evaluation

The evaluator receives:

* Question
* Student Answer
* Retrieved Rubric

Gemini then evaluates the answer strictly according to rubric criteria.

### Example Output

```json
{
  "marks_awarded": 4,
  "max_marks": 5,
  "feedback": "Good explanation but derivation is incomplete.",
  "justification": "The law is correctly defined, but intermediate derivation steps are missing."
}
```

---

## ⚙️ Tech Stack

| Component     | Technology    |
| ------------- | ------------- |
| Frontend      | Streamlit     |
| Backend       | FastAPI       |
| LLM Framework | LangChain     |
| AI Model      | Google Gemini |
| Validation    | Pydantic      |
| Language      | Python        |

---

## 📡 API Endpoint

### POST /evaluate

### Request

```json
{
  "question": "State Newton's Second Law of Motion.",
  "student_answer": "Force is proportional to the rate of change of momentum."
}
```

### Response

```json
{
  "marks_awarded": 4,
  "max_marks": 5,
  "feedback": "Correct explanation but formula is missing.",
  "justification": "Student explained the law correctly but did not mention F = ma."
}
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/DevMaheshBatta/Rubic-Evaluator.git
cd Rubic-Evaluator
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### Start FastAPI Server

```bash
uvicorn backend.main:app --reload
```

### Launch Streamlit UI

```bash
streamlit run frontend/app.py
```

---

## 🔮 Future Improvements

* Embedding-Based Rubric Retrieval
* Hybrid Search (Keywords + Embeddings)
* Teacher Dashboard
* Batch Evaluation
* Student Analytics
* Multi-Language Support
* Rubric Management Portal

---

## 🎯 Key Learnings

* FastAPI API Development
* LangChain Workflows
* Prompt Engineering
* Gemini Integration
* Structured LLM Outputs
* Educational AI Systems
* Rubric-Grounded Evaluation

---

## 👨‍💻 Author

**Dev Mahesh Batta**

Computer Science Engineer | AI & Machine Learning Enthusiast

GitHub: https://github.com/DevMaheshBatta

---

⭐ If you found this project useful, consider giving it a star.
