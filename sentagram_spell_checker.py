import csv
from difflib import get_close_matches
import zemberek_spell_checker as zsc


def print_result(result):
    if result['is_correct']:
        print(f"'{result['word']}' doğru yazılmış.")
    else:
        print(f"'{result['word']}' yanlış yazılmış olabilir. Öneriler: {', '.join(result['suggestion_or_word'])}")


class SentagramSpellChecker:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.words = {}
        self.load_csv(csv_file)

    def load_csv(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = row['madde'].lower()
                meaning = row['anlam']
                if word not in self.words:
                    self.words[word] = []
                self.words[word].append(meaning)

    def write_csv(self, csv_file, word):
        with open(csv_file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['madde', 'anlam'])
            writer.writerows(word)


    def check_word(self, word):
        word = word.lower()
        if word in self.words:
            return True, word, self.words[word]
        else:
            zemberek_suggestions = zsc.check_spelling(word)
            if word in zemberek_suggestions:
                self.write_csv(self.csv_file, word)
                if word not in self.words:
                    self.words[word] = []
                self.words[word].append("")
                return True, word, self.words[word]
            else:
                suggestions = get_close_matches(word, self.words.keys(), n=3, cutoff=0.8)
                return False, suggestions, None

    def check_text(self, text):
        words = text.split()
        results = []
        for word in words:
            is_correct, suggestion_or_word, meanings = self.check_word(word)
            results.append({
                'word': word,
                'is_correct': is_correct,
                'suggestion_or_word': suggestion_or_word,
                'meanings': meanings
            })
        return results


if __name__ == '__main__':
    ssc = SentagramSpellChecker('data/tdk_word_meaning_data.csv')
    text = "Merheba dünye, bu bir örnek cümle."
    results = ssc.check_text(text)
    print(results)
