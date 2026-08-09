import os
import time
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

# Ətraf mühit dəyişənlərini yüklə
load_dotenv()

# Token qiymətləri (məsələn, GPT-4o-mini üçün standart qiymətlər)
INPUT_TOKEN_COST_PER_1K = 0.00015
OUTPUT_TOKEN_COST_PER_1K = 0.0006


@dataclass
class EvaluationMetric:
    prompt: str
    expected_output: str
    actual_output: str
    passed: bool
    latency_seconds: float
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float


class LLMTracker:

    def __init__(self):
        self.metrics: List[EvaluationMetric] = []

    def calculate_cost(self, prompt_tokens: int,
                       completion_tokens: int) -> float:
        input_cost = (prompt_tokens / 1000) * INPUT_TOKEN_COST_PER_1K
        output_cost = (completion_tokens / 1000) * OUTPUT_TOKEN_COST_PER_1K
        return input_cost + output_cost

    def mock_llm_call(self, prompt: str) -> tuple[str, int, int]:
        """LLM sorğusunu simulyasiya edir (və ya real API çağırışı ilə əvəz edilə bilər)."""
        time.sleep(0.35)  # Latency simulyasiyası
        simulated_response = "Baku"
        prompt_tokens = len(prompt.split()) * 2
        completion_tokens = len(simulated_response.split()) * 2
        return simulated_response, prompt_tokens, completion_tokens

    def evaluate_test_case(self, prompt: str, expected: str):
        start_time = time.perf_counter()

        # LLM çağırışı
        response, p_tokens, c_tokens = self.mock_llm_call(prompt)

        latency = time.perf_counter() - start_time
        passed = (response.strip().lower() == expected.strip().lower())
        cost = self.calculate_cost(p_tokens, c_tokens)

        metric = EvaluationMetric(
            prompt=prompt,
            expected_output=expected,
            actual_output=response,
            passed=passed,
            latency_seconds=latency,
            prompt_tokens=p_tokens,
            completion_tokens=c_tokens,
            cost_usd=cost,
        )
        self.metrics.append(metric)

    def print_summary(self):
        if not self.metrics:
            print("Heller qiymətləndirmə aparılmayıb.")
            return

        total_tests = len(self.metrics)
        passed_tests = sum(1 for m in self.metrics if m.passed)
        accuracy = (passed_tests / total_tests) * 100
        avg_latency = sum(m.latency_seconds
                          for m in self.metrics) / total_tests
        avg_cost = sum(m.cost_usd for m in self.metrics) / total_tests
        total_cost = sum(m.cost_usd for m in self.metrics)

        print("\n" + "=" * 45)
        print("  NƏTİCƏ VƏ METRİKLƏR (SUMMARY)")
        print("=" * 45)
        print(
            f"  Accuracy / Pass-Rate : {accuracy:.2f}% ({passed_tests}/{total_tests})"
        )
        print(f"   Orta Latency         : {avg_latency:.4f} saniyə")
        print(f"  Orta Token Xərci     : ${avg_cost:.6f}")
        print(f"  Ümumi Token Xərci    : ${total_cost:.6f}")
        print("=" * 45)


if __name__ == "__main__":
    tracker = LLMTracker()

    test_dataset = [
        {
            "prompt": "Azerbaycanin paytaxti haradir?",
            "expected": "Baku"
        },
        {
            "prompt": "Fransanin paytaxti haradir?",
            "expected": "Paris"
        },
        {
            "prompt": "Turkiyenin paytaxti haradir?",
            "expected": "Ankara"
        },
    ]

    for item in test_dataset:
        tracker.evaluate_test_case(item["prompt"], item["expected"])

    tracker.print_summary()
