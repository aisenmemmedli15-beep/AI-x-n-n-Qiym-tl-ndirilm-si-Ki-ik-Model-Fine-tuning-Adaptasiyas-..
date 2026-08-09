import os
import time
from dataclasses import dataclass
from typing import Dict, List
from dotenv import load_dotenv

# Ətraf mühit dəyişənlərini yüklə
load_dotenv()


@dataclass
class ComparisonResult:
    test_id: int
    user_query: str
    expected_output: str
    before_fix_output: str
    after_fix_output: str
    before_passed: bool
    after_passed: bool


class PromptOptimizer:

    def __init__(self):
        self.results: List[ComparisonResult] = []

    def mock_baseline_llm(self, query: str) -> str:
        """Düzəlişdən əvvəlki (baza) zəif prompt ilə verilən cavab simulyasiyası."""
        if "məhsul" in query.lower():
            return "Məhsul yaxşıdır və müxtəlif özəllikləri var."
        elif "müştəri" in query.lower():
            return "Müştərilər bizdən razıdır."
        return "Məlumat yoxdur."

    def mock_optimized_llm(self, query: str) -> str:
        """Few-Shot Prompt və struktur təlimatları əlavə edildikdən sonrakı cavab simulyasiyası."""
        if "məhsul" in query.lower():
            return "【MƏHSUL HAQQINDA MƏLUMAT】\n• Adı: Smart-TV X\n• Qiymət: 1200 AZN\n• Özəlliklər: 4K Ultra HD, OLED panel, 120Hz refresh rate."
        elif "müştəri" in query.lower():
            return "【MÜŞTƏRİ MƏMNUNİYYƏTİ HESABATI】\n• Ümumi Reytinq: 4.8/5\n• Əsas Rəylər: Çatdırılma sürətlidir, keyfiyyət yüksəkdir."
        return "Sual anlaşılmadı, xahiş olunur dəqiqləşdirin."

    def run_comparison(self, dataset: List[Dict]):
        """Əvvəl və sonra nəticələrini müqayisə edir."""
        for item in dataset:
            query = item["query"]
            expected = item["expected"]

            before_out = self.mock_baseline_llm(query)
            after_out = self.mock_optimized_llm(query)

            # Meyar: Cavabın strukturlaşdırılmış və detallı olması
            before_passed = len(before_out.split("\n")) > 2
            after_passed = len(after_out.split("\n")) > 2

            res = ComparisonResult(
                test_id=item["id"],
                user_query=query,
                expected_output=expected,
                before_fix_output=before_out,
                after_fix_output=after_out,
                before_passed=before_passed,
                after_passed=after_passed,
            )
            self.results.append(res)

    def print_comparison_report(self):
        """Müqayisəli hesabatı çap edir."""
        print("\n" + "=" * 70)
        print("  PROMPT OPTİMALLAŞDIRILMASI: ƏVVƏL / SONRA MÜQAYİSƏ HESABATI")
        print("=" * 70)

        for r in self.results:
            print(f"\n  Test #{r.test_id} | Sorğu: '{r.user_query}'")
            print(f"  [ƏVVƏL - Baza Prompt]:\n{r.before_fix_output}")
            print(
                f"  [SONRA - Optimizə Edilmiş Few-Shot Prompt]:\n{r.after_fix_output}"
            )
            print("-" * 70)

        total = len(self.results)
        before_acc = (sum(1 for r in self.results if r.before_passed) /
                      total) * 100
        after_acc = (sum(1 for r in self.results if r.after_passed) /
                     total) * 100

        print("\n  NƏTİCƏLƏRİN MÜQAYİSƏSİ:")
        print(
            f"• Düzəlişdən əvvəlki dəqiqlik/uyğunluq (Pass-Rate) : {before_acc:.1f}%"
        )
        print(
            f"• Düzəlişdən sonrakı dəqiqlik/uyğunluq (Pass-Rate) : {after_acc:.1f}%"
        )
        print(
            f"  Performans artımı                             : +{after_acc - before_acc:.1f}%"
        )
        print("=" * 70)


if __name__ == "__main__":
    optimizer = PromptOptimizer()

    test_cases = [{
        "id": 1,
        "query": "Məhsul haqqında məlumat ver.",
        "expected": "Strukturlaşdırılmış məhsul parametri və siyahısı.",
    }, {
        "id": 2,
        "query": "Müştəri rəylərini xülasə et.",
        "expected": "Strukturlaşdırılmış reytinq və rəy siyahısı.",
    }]

    optimizer.run_comparison(test_cases)
    optimizer.print_comparison_report()
