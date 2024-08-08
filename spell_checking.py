from sentagram_spell_checker import SentagramSpellChecker
import zemberek_spell_checker


def check(text):
    ssc = SentagramSpellChecker('data/tdk_word_meaning_data.csv')
    results = ssc.check_text(text)
    print(results)


if __name__ == '__main__':
    test_text = "Merheba dünye, bu bir örnek cümle."
    check(test_text)
