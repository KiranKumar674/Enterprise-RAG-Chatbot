
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retriever import retrieve_documents
from rag_pipeline import answer_question


RETRIEVAL_CASES = [
    {
        "question": "How often are performance reviews conducted?",
        "role": "hr",
        "expected_fact": "twice per year",
    },
    {
        "question": "How many working days does reimbursement processing take?",
        "role": "finance",
        "expected_fact": "five working days",
    },
    {
        "question": "What is the IT support schedule?",
        "role": "general",
        "expected_fact": "monday to friday",
    },
]

ANSWER_CASES = [
    {
        "question": "How often are performance reviews conducted?",
        "role": "hr",
        "expected": "twice per year",
    },
    {
        "question": "How many working days does reimbursement processing take?",
        "role": "finance",
        "expected": "five working days",
    },
    {
        "question": "What is the company's maternity leave duration?",
        "role": "hr",
        "expected": None,
    },
]


def evaluate_retrieval():
    results = []

    for case in RETRIEVAL_CASES:
        documents = retrieve_documents(
            case["question"],
            role=case["role"],
            n_results=3,
        )

        retrieved_text = "\n".join(documents).lower()
        hit = case["expected_fact"] in retrieved_text

        results.append({
            "question": case["question"],
            "role": case["role"],
            "expected_fact": case["expected_fact"],
            "hit": hit,
            "retrieved_chunks": len(documents),
        })

        print(f"\nRetrieval question: {case['question']}")
        print(f"Hit: {'YES' if hit else 'NO'}")

    hit_rate = (
        sum(result["hit"] for result in results) / len(results) * 100
        if results else 0.0
    )

    return {
        "questions_evaluated": len(results),
        "hits": sum(result["hit"] for result in results),
        "hit_rate_at_3_percent": round(hit_rate, 2),
        "details": results,
    }


def evaluate_answers():
    results = []

    for case in ANSWER_CASES:
        answer = answer_question(
            case["question"],
            role=case["role"],
        )

        normalized_answer = answer.lower()

        if case["expected"] is not None:
            passed = case["expected"] in normalized_answer
        else:
            uncertainty_phrases = [
                "not provide enough information",
                "couldn't find relevant information",
                "don't have enough information",
                "do not have enough information",
            ]
            passed = any(
                phrase in normalized_answer
                for phrase in uncertainty_phrases
            )

        results.append({
            "question": case["question"],
            "role": case["role"],
            "expected": case["expected"],
            "answer": answer,
            "passed": passed,
        })

        print(f"\nAnswer question: {case['question']}")
        print(f"Answer: {answer}")
        print(f"Evaluation: {'PASS' if passed else 'CHECK'}")

    passed_count = sum(result["passed"] for result in results)

    pass_rate = (
        passed_count / len(results) * 100
        if results else 0.0
    )

    return {
        "questions_evaluated": len(results),
        "passed": passed_count,
        "pass_rate_percent": round(pass_rate, 2),
        "details": results,
    }


def main():
    print("\n===== RAG Evaluation Started =====")

    retrieval_report = evaluate_retrieval()
    answer_report = evaluate_answers()

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "retrieval_evaluation": retrieval_report,
        "answer_evaluation": answer_report,
    }

    output_path = PROJECT_ROOT / "logs" / "evaluation_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print("\n===== Combined RAG Evaluation Report =====")
    print(
        f"Retrieval Hit Rate@3: "
        f"{retrieval_report['hit_rate_at_3_percent']:.2f}%"
    )
    print(
        f"Answer Pass Rate: "
        f"{answer_report['pass_rate_percent']:.2f}%"
    )
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
