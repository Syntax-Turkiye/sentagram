import jpype
import jpype.imports
from jpype.types import *

# JVM'i başlat ve Zemberek JAR dosyasını yükle
# jpype.startJVM(classpath=['zemberek-full.jar'])

# Gerekli Java sınıflarını import et
from zemberek.morphology import TurkishMorphology
from zemberek.normalization import TurkishSpellChecker

# TurkishMorphology nesnesini oluştur
morphology = TurkishMorphology.create_with_defaults()

# TurkishSpellChecker nesnesini oluştur
spell_checker = TurkishSpellChecker(morphology)


def check_spelling(word):
    suggestions = spell_checker.suggest_for_word(word)
    python_suggestions = [str(suggestion) for suggestion in suggestions]
    return python_suggestions


if __name__ == '__main__':
    print(check_spelling("Dünye"))
    print()
