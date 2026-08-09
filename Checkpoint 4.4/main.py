import os
import time
from dataclasses import dataclass, asdict
from typing import List, Optional
from dotenv import load_dotenv

# Ətraf mühit dəyişənlərini yüklə
load_dotenv()


@dataclass
class FailureAnalysis:
    case_id: int
    user_query: str
    expected_output: str
    actual_output: str
    failure_category: str  # Zəif Retrieval, Zəif Prompt, Qeyri-müəyyən Sual
    root_cause: str
    recommended_fix: str


class SystemEvaluator:

    def __init__(self):
        self.failure_cases: List[FailureAnalysis] = []

    def log_failure(self, case: FailureAnalysis):
        """Uğursuzluq halını sistemə qeyd edir."""
        self.failure_cases.append(case)

    def print_root_cause_report(self):
        """Kök-səbəb analizinin nəticələrini hesabat şəklində çap edir."""
        print("\n" + "=" * 65)
        print("🔍 UĞURSUZLUQ HALININ KÖK-SƏBƏB ANALİZİ HESABATI")
        print("=" * 65)

        for case in self.failure_cases:
            print(f"\n  Case ID           : {case.case_id}")
            print(f"  Sorğu            : {case.user_query}")
            print(f"  Gözlənilən       : {case.expected_output}")
            print(f"  Alınan Cavab     : {case.actual_output}")
            print(f"   Kateqoriya       : {case.failure_category}")
            print(f"  Kök-Səbəb        : {case.root_cause}")
            print(f"   Təklif Edilən Həll: {case.recommended_fix}")
            print("-" * 65)


if __name__ == "__main__":
    evaluator = SystemEvaluator()

    # Case 1: Zəif Retrieval (Poor Retrieval)
    evaluator.log_failure(
        FailureAnalysis(
            case_id=1,
            user_query="Şirkətin 2024-cü il 2-ci rüb gəliri nə qədər olub?",
            expected_output="1.2 milyon AZN",
            actual_output="Məlumat tapılmadı.",
            failure_category="Zəif Retrieval (Poor Retrieval)",
            root_cause=
            "Vektor verilənlər bazasında 2024 Q2 maliyyə hesabatı indekslənməyib və çunk ölçüsü (chunk size) çox kiçik seçildiyi üçün müvafiq sənəd semantik axtarışda tapılmayıb.",
            recommended_fix=
            "Chunk ölçüsünü 512 tokenə qaldırmaq və hybrid search (BM25 + Dense Retrieval) tətbiq etmək.",
        ))

    # Case 2: Zəif Prompt (Poor Prompting)
    evaluator.log_failure(
        FailureAnalysis(
            case_id=2,
            user_query="Məhsul haqqında məlumat ver.",
            expected_output=
            "Məhsulun xüsusiyyətləri, qiyməti və istifadə sahələri üzrə strukturlaşdırılmış siyahı.",
            actual_output="Məhsul yaxşıdır və bir çox xüsusiyyətləri var.",
            failure_category=
            "Zəif Prompt (Poor Prompting / System Instruction)",
            root_cause=
            "System prompt-da cavabın formatı, rolu və cavablandırma qaydaları (few-shot examples) aydın şəkildə müəyyən edilməyib.",
            recommended_fix=
            "System prompt-a Few-Shot nümunələri və strukturlaşdırılmış Markdown/JSON format tələbi əlavə etmək.",
        ))

    # Case 3: Qeyri-müəyyən Sual (Ambiguous Query)
    evaluator.log_failure(
        FailureAnalysis(
            case_id=3,
            user_query="Növbəti görüş nə vaxtdır?",
            expected_output="Görüşün dəqiq tarixi, vaxtı və mövzusu.",
            actual_output="Görüş sabah saat 10:00-dadır.",
            failure_category="Qeyri-müəyyən Sual (Ambiguous Query)",
            root_cause=
            "İstifadəçi hansı layihə və ya komandanın görüşü olduğunu qeyd etməyib. Modellə əvvəlki kontekst (session state) paylaşılmayıb.",
            recommended_fix=
            "İstifadəçiyə dəqiqləşdirici sual vermək üçün 'Clarification Intent' mərhələsi əlavə etmək.",
        ))

    evaluator.print_root_cause_report()
