## Layihə haqqında Ümumi Məlumat və Məqsəd
Süni intellekt sistemlərinin (böyük dil modelləri (LLM), RAG mühərrikləri və avtonom AI Agentləri) real istifadə mühitinə (production) inteqrasiyası zamanı ən kritik problemlərdən biri onların çıxış keyfiyyətinin, faktoloji dəqiqliyinin və etibarlılığının ölçülməsidir. Ənənəvi proqram təminatı testləri (unit testing) açıq-uclu (open-ended) AI cavablarını qiymətləndirməkdə yetərsiz qalır.

Bu layihənin əsas məqsədi LLM Evaluation Framework quraraq AI çıxışlarını tam avtomatlaşdırılmış şəkildə test etmək, keyfiyyət və resurs metriklərini ölçmək və sistemdəki zəiflikləri aşkar edərək optimallaşdırmaqdır.

##  Layihənin Əsas Hədəfləri:
İkili Qiymətləndirmə Metodologiyası: Boş sorğular və qəti eynilik tələb olunan hallar üçün Exact Match, açıq-uclu mürəkkəb cavablar üçün isə LLM-as-a-Judge mexanizminin tətbiqi.

Kənar Halların (Edge Cases) Test Edilməsi: Yalnız standart (normal) sualları deyil, out-of-domain, false-premise, prompt-injection və noisy-text kimi riskli kənar halları əhatə edən 15–20 suallıq benchmark dataset üzərində sistemi sınamaq.

LLM Qərəzliliyinin (Bias Mitigation) Qarşısının Alınması: Hakim model kimi çıxış edən LLM-in uzun və bəlağətli cavablara meylliliyini (Verbosity Bias) önləmək üçün sərt qiymətləndirmə rubrikası və JSON çıxış standartı tətbiq etmək.

Kritik Metriklərin İzlənilməsi: Real vaxt rejimində sistemin Accuracy / Pass-Rate (%), Latency (gecikmə saniyəsi) və Token Xərci ($ USD) göstəricilərini çıxarmaq.

Kök-Səbəb Analizi (Root Cause Analysis): Uğursuz olan (FAIL alan) testlərin hansı səbəbdən (zəif retrieval, hallüsinasiya, qeyri-müəyyənlik) qaynaqlandığını təhlil edib optimallaşdırma strategiyası formalaşdırmaq.
