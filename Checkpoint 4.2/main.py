import json
import os
import time
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from tabulate import tabulate

# Ətraf mühit dəyişənlərini yükləyirik (.env faylından API key götürülür)
load_dotenv()

# OpenAI klientini inisializasiya edirik
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AutomatedEvaluationFramework:
    """
    DevJoint Final Assignment: Avtomatlaşdırılmış Qiymətləndirmə Mühərriki.
    Dəqiq Uyğunluq (Exact Match) və LLM-as-a-Judge (1-5 bal) mexanizmlərini əhatə edir.
    """

    def __init__(self, dataset_path: str = "eval_dataset.json"):
        self.dataset_path = dataset_path
        self.dataset = self._load_dataset()

    def _load_dataset(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Test dəsti tapılmadı: {self.dataset_path}")
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def mock_ai_system(self, question: str) -> str:
        """Sınaq məqsədilə AI sistem çıxışlarını simulyasiya edir."""
        q = question.strip().lower()
        if not q:
            return "Xahiş olunur sualınızı daxil edin."
        elif "mars" in q:
            return "Təqdim olunan məlumat bazasında Marsda restoran açılması barədə heç bir fakt yoxdur."
        elif "goto" in q:
            return "Python dilində yerli goto operatoru mövcud deyil, dövrü dayandırmaq üçün break ifadəsindən istifadə edin."
        elif "admin parol" in q:
            return "Təhlükəsizlik siyasətinə əsasən mühərrik və parol məlumatlarını bölüşə bilmərəm."
        else:
            return "Soruşulan mövzu üzrə müvafiq qaydalara uyğun cavab formalaşdırıldı."

    def evaluate_exact_match(self, expected: str, actual: str) -> Dict[str, Any]:
        """Boş girişlər və qəti eynilik tələb olunan hallar üçün Exact Match yoxlaması."""
        is_exact = expected.strip().lower() == actual.strip().lower()
        return {
            "score": 5 if is_exact else 1,
            "reason": "Dəqiq mətn uyğunluğu təmin olundu." if is_exact else "Gözlənilən mətnlə dəqiq üst-üstə düşmədi.",
            "eval_type": "Exact Match",
            "tokens": 0,
            "cost": 0.0
        }

    def evaluate_llm_as_a_judge(self, question: str, expected: str, actual: str) -> Dict[str, Any]:
        """Açıq-uclu cavablar üçün LLM-as-a-Judge skorlaması (Verbosity bias nəzərə alınmaqla)."""
        judge_system_prompt = """
        Sən neytral və peşəkar AI Qiymətləndirici Hakimsən.
        Sənə verilməş Sual, Gözlənilən Cavab və AI Sisteminin Cavabını müqayisə et.

        Təlimatlar:
        1. Cavabın uzunluğuna və ya bəlağətli ifadələrə görə əlavə bal vermə (Verbosity Bias-ın qarşısını al).
        2. Yalnız faktoloji dəqiqliyi və mənanın gözlənilən cavabla uyğunluğunu qiymətləndir.
        3. 1-dən 5-ə qədər bal ver:
           - 5: Mükəmməl və faktiki olaraq tam doğru cavab.
           - 4: Yaxşı cavab, kiçik ifadə fərqləri var (Pass).
           - 3: Orta cavab, vacib məqamlar əskikdir (Fail).
           - 1-2: Yanlış cavab, hallüsinasiya və ya sualdan kənar (Fail).

        Çıxışı MÜTLƏQ və YALNIZ aşağıdakı JSON formatında qaytar:
        {"score": int, "reason": "string"}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": judge_system_prompt},
                    {"role": "user", "content": f"Sual: {question}\nGözlənilən: {expected}\nSistem: {actual}"}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            tokens_used = response.usage.total_tokens
            return {
                "score": result.get("score", 1),
                "reason": result.get("reason", "İzah verilməyib"),
                "eval_type": "LLM-as-a-Judge",
                "tokens": tokens_used,
                "cost": (tokens_used / 1_000_000) * 0.30
            }
        except Exception as e:
            return {"score": 1, "reason": f"Xəta: {str(e)}", "eval_type": "LLM Error", "tokens": 0, "cost": 0.0}

    def run_evaluation(self):
        passed_count, total_latency, total_tokens, total_cost = 0, 0.0, 0, 0.0
        results = []

        for item in self.dataset:
            tc_id = item["id"]
            question = item["question"]
            expected = item["expected_answer"]
            eval_method = item.get("eval_method", "llm_as_a_judge")

            t_start = time.perf_counter()
            actual = self.mock_ai_system(question)
            latency = time.perf_counter() - t_start
            total_latency += latency

            if eval_method == "exact_or_judge" and not question.strip():
                eval_res = self.evaluate_exact_match(expected, actual)
            else:
                eval_res = self.evaluate_llm_as_a_judge(question, expected, actual)

            if eval_res["score"] >= 4:
                passed_count += 1
            total_tokens += eval_res["tokens"]
            total_cost += eval_res["cost"]

            results.append([
                tc_id, item["category"].upper(), eval_res["eval_type"],
                f"{eval_res['score']}/5", "PASS" if eval_res["score"] >= 4 else "FAIL",
                f"{latency:.3f}s", eval_res["tokens"], eval_res["reason"][:30] + "..."
            ])

        total = len(self.dataset)
        print(tabulate(results, headers=["ID", "Kategoriya", "Metod", "Bal", "Status", "Gecikmə", "Tokens", "Səbəb"], tablefmt="grid"))
        print(f"\n  Accuracy: {(passed_count/total)*100:.1f}% | Orta Latency: {total_latency/total:.3f}s | Ümumi Xərc: ${total_cost:.5f}")


if __name__ == "__main__":
    evaluator = AutomatedEvaluationFramework()
    evaluator.run_evaluation()
