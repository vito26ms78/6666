import re
from deep_translator import GoogleTranslator
from cache.translation_cache import TranslationCache

class TranslatorEngine:

    def __init__(self):
        self.translator = GoogleTranslator(source="auto", target="zh-TW")
        self.cache = TranslationCache()

    def normalize(self, text):
        text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def translate(self, text):
        text = str(text).strip()
        normalized = self.normalize(text)

        if not normalized:
            return text

        cached = self.cache.get(normalized)
        if cached:
            return cached

        try:
            translated = self.translator.translate(normalized)
            self.cache.set(normalized, translated)
            return translated
        except Exception:
            return text
