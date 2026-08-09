##  Layihənin Məqsədi
Bu layihə Dil Modellerinin (LLM) performansını və resurs effektivliyini real vaxt rejimində izləmək üçün hazırlanmışdır. Layihə sistemin dəqiqliyini, cavabvermə sürətini və malıyyə xərclərini ölçərək modelin optimallaşdırılmasına kömək edir.

##  Layihə Haqqında Məlumat
Sistem test məlumat dəsti əsasında modelə sorğular göndərir və 3 əsas metriki hesablayaraq hesabat təqdim edir:
1. **Accuracy / Pass-Rate:** Modelin düzgün verdiyi cavabların faiz göstəricisi.
2. **Orta Latency (Gecikmə):** Hər bir sorğunun emal edilməsi üçün tələb olunan orta zaman (saniyə ilə).
3. **Orta Token Xərci:** İstifadə olunan prompt və completion tokenlərinə əsasən hər sorğuya düşən orta xərc ($ USD ilə).
