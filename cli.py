#!/usr/bin/env python3
"""
cli.py  —  Command-line interface for Rubic-Evaluator
-----------------------------------------------------------
Usage:
  python cli.py
  python cli.py --compare        # also show evaluation without rubric
  python cli.py --question "..." --answer "..."
"""

import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rubrics.rubric_retriever import retrieve_rubric
from backend.evaluator import evaluate_with_rubric, evaluate_without_rubric


# ── Colours ───────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GRAY   = "\033[90m"
BLUE   = "\033[94m"
PURPLE = "\033[95m"


def _color(text, *codes):
    return "".join(codes) + str(text) + RESET


def _bar(marks, max_marks, width=20):
    filled = int((marks / max_marks) * width) if max_marks else 0
    color  = GREEN if marks == max_marks else YELLOW if marks >= max_marks / 2 else RED
    return _color("█" * filled, color) + _color("░" * (width - filled), GRAY)


def print_rubric(rubric: dict):
    print(_color("\n  📋 RETRIEVED RUBRIC", BOLD, CYAN))
    print(f"  Subject : {_color(rubric['subject'], BOLD)} ({rubric['level']})")
    print(f"  Rubric  : {rubric['id']}")
    is_fb = rubric["id"] == "generic_fallback"
    match_info = (
        _color("⚠ Fallback (no keyword match)", YELLOW)
        if is_fb
        else _color(f"✓ Keyword match (score {rubric.get('_match_score', 0)})", GREEN)
    )
    print(f"  Match   : {match_info}")
    print(f"  Marks   : {rubric['max_marks']}")
    print(f"\n  {_color('Criteria:', BOLD)}")
    for i, c in enumerate(rubric["criteria"], 1):
        print(
            f"    {_color(i, GRAY)}. [{_color(c['max_marks'], BOLD)} mk] "
            f"{_color(c['name'], BOLD)} — {c['description']}"
        )
    print()


def print_result(result: dict, title: str = "EVALUATION"):
    marks = result["marks_awarded"]
    max_m = result["max_marks"]
    pct = int((marks / max_m) * 100)
    score_color = GREEN if pct >= 70 else YELLOW if pct >= 40 else RED

    print(_color(f"\n  🏆 {title}", BOLD, PURPLE))
    print(f"  Score      : {_color(f'{marks}/{max_m}', BOLD, score_color)}  {_bar(marks, max_m)}  {_color(f'{pct}%', score_color)}")
    print(f"\n  {_color('Feedback:', BOLD, GREEN)}")
    print(f"  {result['feedback']}")
    print(f"\n  {_color('Justification:', BOLD, YELLOW)}")
    print(f"  {result['justification']}")

    breakdown = result.get("criteria_breakdown", [])
    if breakdown:
        print(f"\n  {_color('Marks Breakdown:', BOLD)}")
        for c in breakdown:
            b = _bar(c["marks_given"], c["max"], width=10)
            print(
                f"    {_color(c['criterion'], BOLD)}: {_color(c['marks_given'], BOLD)}/{c['max']}  "
                f"{b}  {_color(c['comment'], GRAY)}"
            )
    print()


def run_evaluation(question: str, answer: str, compare: bool):
    print(_color("\n════════════════════════════════════════", CYAN))
    print(_color("         RUBRIC-EVALUATOR", BOLD, CYAN))
    print(_color("════════════════════════════════════════", CYAN))

    print(f"\n  {_color('Question:', BOLD)}\n  {question}")
    print(f"\n  {_color('Answer:', BOLD)}\n  {answer}\n")

    # Step 1: Retrieve rubric
    print(_color("  ⟳ Retrieving rubric…", GRAY))
    rubric = retrieve_rubric(question)
    print_rubric(rubric)

    # Step 2: Evaluate with rubric
    print(_color("  ⟳ Evaluating with rubric (calling )…", GRAY))
    result_with = evaluate_with_rubric(question, answer, rubric)
    print_result(result_with, "EVALUATION (with rubric)")

    # Step 3 (optional): Without rubric
    if compare:
        print(_color("  ⟳ Evaluating without rubric (comparison)…", GRAY))
        result_without = evaluate_without_rubric(question, answer)
        print_result(result_without, "EVALUATION (without rubric — comparison)")

        # Diff summary
        diff = result_with["marks_awarded"] - result_without["marks_awarded"]
        diff_str = (
            _color(f"+{diff}", GREEN) if diff > 0
            else _color(str(diff), RED) if diff < 0
            else _color("0 (same)", GRAY)
        )
        print(_color("  📊 COMPARISON SUMMARY", BOLD, BLUE))
        print(f"  With rubric   : {result_with['marks_awarded']}/{result_with['max_marks']}")
        print(f"  Without rubric: {result_without['marks_awarded']}/{result_without['max_marks']}")
        print(f"  Difference    : {diff_str}")
        print()

    print(_color("════════════════════════════════════════\n", CYAN))


def main():
    parser = argparse.ArgumentParser(description="Rubric-Evaluator CLI")
    parser.add_argument("--question", "-q", type=str, help="Exam question")
    parser.add_argument("--answer",   "-a", type=str, help="Student's answer")
    parser.add_argument("--compare",  "-c", action="store_true",
                        help="Also evaluate without rubric for comparison")
    args = parser.parse_args()

    if args.question and args.answer:
        run_evaluation(args.question, args.answer, args.compare)
        return

    # Interactive mode
    print(_color("\n  🎓 Rubric-Evaluator — Interactive Mode", BOLD, CYAN))
    print(_color("  (Ctrl+C to exit)\n", GRAY))

    while True:
        try:
            question = input(_color("  Enter question: ", BOLD)).strip()
            if not question:
                continue
            answer = input(_color("  Enter answer  : ", BOLD)).strip()
            if not answer:
                continue
            compare = args.compare or input(
                _color("  Compare with/without rubric? (y/N): ", GRAY)
            ).strip().lower() == "y"

            run_evaluation(question, answer, compare)

            again = input(_color("  Evaluate another? (y/N): ", GRAY)).strip().lower()
            if again != "y":
                break
        except KeyboardInterrupt:
            print(_color("\n\n  Goodbye!\n", GRAY))
            break


if __name__ == "__main__":
    main()
