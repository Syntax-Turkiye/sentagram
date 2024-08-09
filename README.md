# synturk-sentagram
#Acıkhack2024TTDİ

# SENTAGRAM

SENTAGRAM, Türkçe cümlelerin dil bilgisi ögelerini ayırmak ve analiz etmek için geliştirilmiş bir uygulamadır. Proje, BERTürk tabanlı bir model kullanarak cümlelerdeki özneleri, yüklemleri, tümleçleri ve diğer dil bilgisi yapılarını ayırır ve bu ögeler hakkında detaylı bilgi sağlar.

# Motivasyonumuz

Bu modeli oluştururken internet üzerinde bize yardımcı olabilecek herhangi bir veri seti maalesef ki bulamadık. Bu konu hakkında bize öncülük edebilecek bir projeye de rastlayamadık. Türkçemizin zenginliklerini düşününce bizim için zorlu olan bu süreçte, özgün bir proje çıkarma amacıyla yola çıktık.
Türkçe'nin herkes tarafından doğru kullanılması, dil bilgisi kurallarımızın öğrenilmesi ve bilinmesi bizim en büyük hedefimizdir. 

# Özellikler

Dil Bilgisi Analizi: Türkçe cümleleri dil bilgisi kurallarına göre ayrıştırır ve özneleri, yüklemleri, tümleçleri gibi dil bilgisi ögelerini belirler.

Veri Seti: Çeşitli haber siteleri, test kitapları ve makalelerden elde edilen cümleler kullanılarak oluşturulan ve manuel olarak ögelerine ayrılmış veri seti ile eğitilmiştir.

Model Eğitimi: BERTürk tabanlı bir model kullanılarak token sınıflandırma yapılır. Model, Optuna kullanılarak hiperparametre optimizasyonu ile daha iyi performans göstermesi sağlanmıştır.

Performans Metrikleri: Modelin doğruluğunu ve F1 skorunu değerlendirmek için çeşitli metrikler kullanılmıştır.

# Performans

|Training Loss|Validation Loss|Precision|Recall  |F1 Score|Accuracy|
|:-----------:|:-------------:|:-------:|:------:|:------:|:------:|
|0.016700     | 0.479245      |0.911349 |0.911826|0.911588|0.935395| 

# Kurulum

Gereksinimler:
```
Python 3.6+
transformers: Hugging Face'in doğal dil işleme modelleri için kullanılan kütüphane.
datasets: Verileri yüklemek ve işlemek için kullanılan kütüphane.
evaluate: Model performansını değerlendirmek için kullanılan kütüphane.
```
Gerekli Paketlerin Kurulması: SENTAGRAM projesinin çalışması için aşağıdaki paketlerin kurulu olması gerekmektedir. Bu paketler, model eğitimi ve test sürecinde kullanılacaktır.
 pip install transformers datasets evaluate

Veri Setinin Hazırlanması: Verilerinizi dataset.json formatında hazırlayın. Bu dosya, cümlelerin dil bilgisi ögelerine ayrılmış olarak sunulmalıdır.

Modelin Eğitilmesi: Modeli eğitmek için aşağıdaki kodu kullanabilirsiniz. Bu kod, Hugging Face Transformers kütüphanesini kullanarak modelin eğitimini gerçekleştirir.

# Kullanım

Model Yükleme ve Test: Modelinizi test etmek için aşağıdaki örneği kullanabilirsiniz. Bu kod, bir cümleyi modelle test eder ve tahmin edilen etiketleri yazdırır.
```
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

Model ve tokenizer'ı yükle
tokenizer = AutoTokenizer.from_pretrained("path_to_saved_model")
model = AutoModelForTokenClassification.from_pretrained("path_to_saved_model")

Test cümlesi
text = "SYNTÜRK yarışmayı kazandı."

Cümleyi tokenize et
inputs = tokenizer(text, return_tensors="pt")

Model ile tahmin yap
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

Sonuçları yazdır
print(predictions)
```
# Katkıda Bulunanlar
```
Zülfükar MİNAZ
Ayşe Selin ALTUNTAŞ
Ilgın Eylül YILDIZ
Berk İÇLİ
```