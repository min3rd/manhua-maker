from translate import Translator
from modules.core.singleton import Singleton
import argostranslate.package
import argostranslate.translate


class TranslateService(metaclass=Singleton):
    from_code: str
    to_code: str
    translator: Translator

    def __init__(self, from_code: str = "zh", to_code: str = "en"):
        self.from_code = from_code
        self.to_code = to_code
        self.translator = Translator(from_lang=from_code, to_lang=to_code)

    def argostranslate(
        self,
        text: str,
        from_code: str = None,
        to_code: str = None,
    ) -> str:
        if from_code is not None and to_code is not None:
            if self.from_code is not from_code or self.to_code is not to_code:
                self.from_code = from_code
                self.to_code = to_code
                self.translator = Translator(from_lang=from_code, to_lang=to_code)
        return argostranslate.translate.translate(text, from_code, to_code)

    def translate(self, text: str, from_code: str = None, to_code: str = None) -> str:
        if self.from_code is not from_code or self.to_code is not to_code:
            self.from_code = from_code
            self.to_code = to_code
            self.translator = Translator(from_lang=from_code, to_lang=to_code)
        return self.translator.translate(text)
