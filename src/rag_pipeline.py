
import os
from pathlib import Path

from dotenv import load_dotenv #type:ignore
from groq import Groq #type:ignore


try:
    from .monitoring import log_event, calculate_estimated_cost_usd
except ImportError:
    from monitoring import log_event, calculate_estimated_cost_usd


try:
    from .retriever import retrieve_documents
except ImportError:
    from retriever import retrieve_documents

import time

try:
    from .monitoring import log_event
except ImportError:
    from monitoring import log_event


try:
    from .guardrails import (
        detect_sensitive_information,
        is_out_of_scope,
    )
except ImportError:
    from guardrails import (
        detect_sensitive_information,
        is_out_of_scope,
    )


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in the .env file.")

client = Groq(api_key=api_key)


try:
    from .guardrails import detect_sensitive_information, is_out_of_scope
except ImportError:
    from guardrails import detect_sensitive_information, is_out_of_scope




def answer_question(question: str, role: str = "general") -> str:
    start_time = time.perf_counter()
    outcome = "error"
    error_type = None

    prompt_tokens = None
    completion_tokens = None
    estimated_cost_usd = None

    try:
        # Guardrail 1: Reject empty questions.
        if not question or not question.strip():
            outcome = "blocked"
            return "Please enter a question."

        # Guardrail 2: Detect sensitive information.
        sensitive_items = detect_sensitive_information(question)
        if sensitive_items:
            outcome = "blocked"
            return (
                "For your security, this question was blocked because it "
                "may contain sensitive information. Please remove the "
                "sensitive details and try again."
            )

        # Guardrail 3: Reject out-of-scope questions.
        if is_out_of_scope(question):
            outcome = "blocked"
            return (
                "I can only answer questions related to company policies. "
                "Please ask a relevant company-policy question."
            )

        # Step 4: Retrieve documents permitted for this role.
        documents = retrieve_documents(
            question,
            role,
            n_results=2,
        )

        if not documents:
            outcome = "no_context"
            return (
                "I couldn't find relevant information in the documents "
                "you can access."
            )

        context = "\n\n".join(documents)

        # Step 5: Generate an answer using Groq.
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a company policy assistant. Answer using "
                        "only the supplied context. If the context does "
                        "not contain the answer, say that the available "
                        "company documents do not provide enough information. "
                        "Do not invent policies."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Context:\n{context}\n\n"
                        f"Question: {question}\n\n"
                        "Give a concise answer."
                    ),
                },
            ],
            temperature=0,
        )

        
        answer = response.choices[0].message.content

        usage = response.usage

        if usage:
            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens

            estimated_cost_usd = calculate_estimated_cost_usd(
                prompt_tokens,
                completion_tokens,
            )

        if not answer:
            outcome = "empty_response"
            return "No answer was generated."

        outcome = "answered"
        return answer


    except Exception as error:
        error_type = type(error).__name__
        raise

    finally:
        # Record outcome and processing time without logging question text.
        latency_ms = (time.perf_counter() - start_time) * 1000

        
        try:
           log_event(
                    role=role,
                    outcome=outcome,
                    latency_ms=latency_ms,
                    error_type=error_type,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    estimated_cost_usd=estimated_cost_usd,
                )
        except Exception:
            # Logging failures should not hide the original result.
            pass



if __name__ == "__main__":
    print("\nCompany Policy Assistant")
    print("Available test roles: general, hr, finance")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a question: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        role = input("Enter test role (general, hr, finance): ").strip().lower()

        try:
            answer = answer_question(question, role)
            print(f"\nAnswer: {answer}")
        except Exception as error:
            print(f"\nRequest failed: {error}")
