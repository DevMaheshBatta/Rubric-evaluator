"""
app.py  —  Streamlit frontend for Rubic-Evaluator
--------------------------------------------------------
Run with:  streamlit run frontend/app.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import requests

# ── Config ────────────────────────────────────────────────────────────────────

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Rubic — Answer Evaluator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
<style>
    /* Main header */
    .eval-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    .eval-header h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .eval-header p  { margin: 0.3rem 0 0; opacity: 0.75; font-size: 0.95rem; }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .score-big  { font-size: 3.5rem; font-weight: 800; line-height: 1; }
    .score-denom{ font-size: 1.2rem; opacity: 0.8; }
    .score-label{ font-size: 0.85rem; opacity: 0.7; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 0.3rem; }

    /* Feedback box */
    .feedback-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .justification-box {
        background: #fefce8;
        border-left: 4px solid #eab308;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }

    /* Rubric badge */
    .rubric-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        border-radius: 99px;
        padding: 0.2rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .fallback-badge {
        background: #fef3c7;
        color: #92400e;
    }

    /* Criterion row */
    .criterion-row {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid #e5e7eb;
    }
    .criterion-marks {
        min-width: 60px;
        font-weight: 700;
        color: #4f46e5;
        font-size: 1rem;
    }
    .criterion-name { font-weight: 600; font-size: 0.9rem; }
    .criterion-comment { font-size: 0.85rem; color: #6b7280; }

    /* Compare columns */
    .compare-header {
        font-weight: 700;
        font-size: 1rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid;
        margin-bottom: 0.75rem;
    }

    /* Streamlit overrides */
    .stTextArea textarea { font-size: 0.95rem; }
    div[data-testid="stExpander"] { border: 1px solid #e5e7eb; border-radius: 8px; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(
    """
<div class="eval-header">
  <h1>🎓 Rubic-Evaluator</h1>
  <p>Rubric-based LLM evaluation for Class 10–12 answers · Built with FastAPI + LangChain</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Sidebar: Sample questions ─────────────────────────────────────────────────

SAMPLES = {
    "Physics — Newton's Second Law": {
        "question": "State Newton's Second Law of Motion and derive F = ma.",
        "answer": "Newton's Second Law states that the rate of change of momentum of an object is directly proportional to the net force applied. Mathematically, F = dp/dt. For constant mass, p = mv, so F = m(dv/dt) = ma.",
    },
    "Maths — Integration": {
        "question": "Evaluate the integral of x² from 0 to 3.",
        "answer": "∫x² dx = x³/3 + C. Applying limits: [x³/3] from 0 to 3 = 27/3 - 0 = 9.",
    },
    "English — Comprehension": {
        "question": "Explain the theme of courage in the poem 'If' by Rudyard Kipling.",
        "answer": "The poem talks about being brave. The poet says you should keep going even when things are hard. It shows that a real man never gives up.",
    },
    "History — World War I": {
        "question": "What were the main causes of World War I?",
        "answer": "The main causes were nationalism, imperialism, militarism and the alliance system. The assassination of Archduke Franz Ferdinand in 1914 triggered the war. European powers had been building up armies and had formed two rival groups.",
    },
    "Custom question": {"question": "", "answer": ""},
}

with st.sidebar:
    st.subheader("📚 Sample Questions")
    selected_sample = st.selectbox("Load a sample", list(SAMPLES.keys()))
    st.divider()
    compare_mode = st.toggle(
        "🔬 Bonus: Compare with/without rubric",
        value=False,
        help="Runs a second evaluation without any rubric so you can compare the difference",
    )
    st.divider()
    st.caption("Backend: `" + API_URL + "`")

# ── Main form ─────────────────────────────────────────────────────────────────

sample = SAMPLES[selected_sample]

col_q, col_a = st.columns(2)

with col_q:
    st.subheader("❓ Question")
    question = st.text_area(
        "Enter the exam question",
        value=sample["question"],
        height=150,
        placeholder="e.g. State Newton's Second Law and derive F = ma",
        label_visibility="collapsed",
    )

with col_a:
    st.subheader("✍️ Student Answer")
    student_answer = st.text_area(
        "Enter the student's answer",
        value=sample["answer"],
        height=150,
        placeholder="Type the student's answer here…",
        label_visibility="collapsed",
    )

evaluate_btn = st.button("🚀 Evaluate Answer", type="primary", use_container_width=True)

# ── Evaluation ────────────────────────────────────────────────────────────────

if evaluate_btn:
    if not question.strip():
        st.error("Please enter a question.")
        st.stop()
    if not student_answer.strip():
        st.error("Please enter the student's answer.")
        st.stop()

    with st.spinner("Retrieving rubric and evaluating"):
        try:
            resp = requests.post(
                f"{API_URL}/evaluate",
                json={
                    "question": question,
                    "student_answer": student_answer,
                    "compare_mode": compare_mode,
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ Cannot reach the API server. Make sure the FastAPI backend is running:\n\n"
                "```bash\nuvicorn backend.main:app --reload --port 8000\n```"
            )
            st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    rubric = data["rubric"]
    ev = data["evaluation_with_rubric"]

    st.divider()

    # ── Rubric info ──────────────────────────────────────────────────────────

    st.subheader("📋 Retrieved Rubric")
    is_fallback = rubric["id"] == "generic_fallback"
    badge_class = "rubric-badge fallback-badge" if is_fallback else "rubric-badge"
    match_label = (
        "⚠️ Fallback (no subject match)"
        if is_fallback
        else f"✅ Matched — score {rubric['match_score']}"
    )

    st.markdown(
        f"""
<span class="{badge_class}">{rubric['subject']}</span>
<span class="rubric-badge">{rubric['level']}</span>
<span class="rubric-badge">{rubric['max_marks']} marks</span>
<span class="rubric-badge">{match_label}</span>
""",
        unsafe_allow_html=True,
    )

    with st.expander("View rubric criteria"):
        for c in rubric["criteria"]:
            st.markdown(
                f"**{c['name']}** _{c['max_marks']} mark(s)_ — {c['description']}"
            )

    st.divider()

    # ── Evaluation result ────────────────────────────────────────────────────

    if compare_mode and data.get("evaluation_without_rubric"):
        st.subheader("🔬 Comparison: With vs Without Rubric")
        col_with, col_without = st.columns(2)

        for col, eval_data, label, color in [
            (col_with, ev, "WITH Rubric", "#4f46e5"),
            (col_without, data["evaluation_without_rubric"], "WITHOUT Rubric", "#9ca3af"),
        ]:
            with col:
                st.markdown(
                    f'<div class="compare-header" style="border-color:{color};color:{color}">'
                    f"🏷️ {label}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""<div class="score-card">
<div class="score-big">{eval_data['marks_awarded']}</div>
<div class="score-denom">/ {eval_data['max_marks']}</div>
<div class="score-label">marks awarded</div>
</div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="feedback-box">💬 <b>Feedback:</b> {eval_data["feedback"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="justification-box">🧾 <b>Justification:</b> {eval_data["justification"]}</div>',
                    unsafe_allow_html=True,
                )
    else:
        st.subheader("🏆 Evaluation Result")

        col_score, col_detail = st.columns([1, 2])

        with col_score:
            pct = int((ev["marks_awarded"] / ev["max_marks"]) * 100)
            color = (
                "#22c55e" if pct >= 70 else "#eab308" if pct >= 40 else "#ef4444"
            )
            st.markdown(
                f"""<div class="score-card" style="background:{color}">
<div class="score-big">{ev['marks_awarded']}</div>
<div class="score-denom">/ {ev['max_marks']}</div>
<div class="score-label">{pct}% · {ev['subject']}</div>
</div>""",
                unsafe_allow_html=True,
            )

        with col_detail:
            st.markdown(
                f'<div class="feedback-box">💬 <b>Feedback:</b> {ev["feedback"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="justification-box">🧾 <b>Justification:</b> {ev["justification"]}</div>',
                unsafe_allow_html=True,
            )

    # ── Criteria breakdown ───────────────────────────────────────────────────

    if ev.get("criteria_breakdown"):
        st.subheader("📊 Marks Breakdown")
        for c in ev["criteria_breakdown"]:
            pct = int((c["marks_given"] / c["max"]) * 100) if c["max"] else 0
            bar_color = (
                "#22c55e" if pct == 100 else "#eab308" if pct >= 50 else "#ef4444"
            )
            st.markdown(
                f"""<div class="criterion-row">
  <div class="criterion-marks" style="color:{bar_color}">{c['marks_given']}/{c['max']}</div>
  <div>
    <div class="criterion-name">{c['criterion']}</div>
    <div class="criterion-comment">{c['comment']}</div>
  </div>
</div>""",
                unsafe_allow_html=True,
            )
