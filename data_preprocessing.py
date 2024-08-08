import json


def revise_start_end(data):
    for sentence in data['sentences']:
        text = sentence['text']
        for element in sentence['elements']:
            word = element['word']
            element['start'] = text.find(word)
            element['end'] = text.find(word) + len(word) - 1
    return data


class SentagramDataPreprocessing:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def preprocess(self):
        # JSON dosyasını yükleme
        with open(f'{self.file_path}', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # JSON dosyasındaki tekrarlayan verileri temizleme
        unique_sentences = []
        for sentence in data['sentences']:
            text = sentence['text']
            if text not in unique_sentences:
                unique_sentences.append(text)
            else:
                data['sentences'].remove(sentence)

        count = 1
        for sentence in data['sentences']:
            sentence['id'] = count
            for i, element in enumerate(sentence['elements']):
                if "B-" in element['type'] or "I-" in element['type']:
                    continue
                if len(element['word'].split()) == 1:
                    type = element['type'].replace("-", "")
                    element['type'] = 'B-' + type
                else:
                    word = element['word']
                    start = element['start']
                    type = element['type'].replace("-", "")
                    words = word.split()
                    sentence['elements'].remove(element)
                    for j, word in enumerate(words):
                        if j == 0:
                            sentence['elements'].insert(i + j, {'word': word, 'type': 'B-' + type, 'start': start,
                                                                'end': start + len(word)})
                            start = start + len(word) + 1
                        else:
                            sentence['elements'].insert(i + j, {'word': word, 'type': 'I-' + type, 'start': start,
                                                                'end': start + len(word)})
                            start = start + len(word) + 1
            count += 1
        dataset = revise_start_end(data)
        with open(f"{'revised_' + self.file_path}", 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    sdp = SentagramDataPreprocessing('data/aug_aug_1500_ham_veri.json')
    sdp.preprocess()
