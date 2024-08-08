from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import re

# Modeli ve tokenizer'ı yükle
tokenizer = AutoTokenizer.from_pretrained("synturk/sentagram")
model = AutoModelForTokenClassification.from_pretrained("synturk/sentagram")

# Etiket haritasını oluştur
label_map = {
    "B-yuklem": 0,
    "I-yuklem": 1,
    "B-ozne": 2,
    "I-ozne": 3,
    "B-bsiznesne": 4,
    "I-bsiznesne": 5,
    "B-blinesne": 6,
    "I-blinesne": 7,
    "B-dtum": 8,
    "I-dtum": 9,
    "B-ztum": 10,
    "I-ztum": 11,
    "B-etum": 12,
    "I-etum": 13,
    "B-cdıs": 14,
    "I-cdıs": 15
}
id2label = {v: k for k, v in label_map.items()}

# Kullanıcı dostu etiketler
friendly_labels = {
    "yuklem": "Yüklem",
    "ozne": "Özne",
    "bsiznesne": "Belirtisiz Nesne",
    "blinesne": "Belirtili Nesne",
    "dtum": "Dolaylı Tümleç",
    "ztum": "Zarf Tümleci",
    "etum": "Edat Tümleci",
    "cdıs": "Cümle Dışı Unsur"
}


def preprocess_text(text):
    # Orijinal kelimeleri ve preprocess edilmiş hallerini sakla
    original_words = {}
    words = text.split()
    for word in words:
        cleaned_word = re.sub(r"[\.,:;!?]", "", word)
        cleaned_word = re.sub(r"(\w)\'(\w)", r"\1\2", cleaned_word)
        original_words[cleaned_word] = word
    return original_words


def process_sentence(text):
    # Ön işlemden geçir
    original_words = preprocess_text(text)
    cleaned_text = ' '.join(original_words.keys())

    # Cümleyi kelimelere ayır
    words = cleaned_text.split()

    # Cümleyi tokenize et
    inputs = tokenizer(words, return_tensors="pt", is_split_into_words=True, padding=True, truncation=True)

    # Modeli kullanarak tahmin yap
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Tahmin edilen etiketler
    predictions = torch.argmax(logits, dim=2)

    # Tokenleri ve etiketleri çözümle
    word_ids = inputs.word_ids()
    predicted_labels = [id2label[p.item()] for p in predictions[0]]

    # Log: Kelimeler ve etiketler
    for word, label in zip(words, predicted_labels):
        print(f"{word}: {label}")

    # Sonuçları kelimelerle eşleştir ve B- ve I- etiketlerini birleştir
    word_predictions = {}
    current_label = None
    current_words = []
    processed_word_ids = set()  # İşlenmiş kelime id'lerini takip etmek için

    for word_idx, label in zip(word_ids, predicted_labels):
        if word_idx is not None and word_idx not in processed_word_ids:
            processed_word_ids.add(word_idx)  # Kelimenin işlendiğini kaydet
            word = words[word_idx]
            label_prefix, label_type = label.split('-')
            print(f"Processing word: {word}, label: {label}, label_prefix: {label_prefix}, label_type: {label_type}")
            if label_prefix == "B":
                # Yeni bir B- etiketi bulunduğunda önceki tamlamayı ekle
                if current_label and current_words:
                    original_text = ' '.join(original_words[w] for w in current_words)
                    print(f"Tamlamayı ekle: {original_text}: {friendly_labels[current_label]}")
                    word_predictions[original_text] = friendly_labels[current_label]
                # Yeni B- etiketini başlat
                current_label = label_type
                current_words = [word]
                print(f"Yeni B- etiketi başlatıldı: {word}: {current_label}")
            elif label_prefix == "I" and current_label == label_type:
                # I- etiketi mevcut B- etiketiyle uyumluysa kelimeyi ekle
                current_words.append(word)
                print(f"I- etiketi mevcut B- etiketiyle uyumlu: {word}")
            else:
                # Uyumsuz etiket bulunduğunda, mevcut kelimeleri olduğu gibi ekle
                if current_label and current_words:
                    original_text = ' '.join(original_words[w] for w in current_words)
                    print(f"Tamlamayı ekle: {original_text}: {friendly_labels[current_label]}")
                    word_predictions[original_text] = friendly_labels[current_label]
                # Mevcut kelimeyi de ekle
                word_predictions[original_words[word]] = friendly_labels.get(label_type, label_type)
                print(
                    f"Uyumsuz etiket bulundu, mevcut kelime eklendi: {original_words[word]}: {friendly_labels.get(label_type, label_type)}")
                current_label = None
                current_words = []

    # Son tamlamayı ekle
    if current_label and current_words:
        original_text = ' '.join(original_words[w] for w in current_words)
        print(f"Son tamlamayı ekle: {original_text}: {friendly_labels[current_label]}")
        word_predictions[original_text] = friendly_labels[current_label]

    print(word_predictions)

    return word_predictions


# Örnek cümle
text = "Selin Bodrum'a gitti."
result = process_sentence(text)

# Sonuçları yazdır
for word, label in result.items():
    print(f"{word}: {label}")
