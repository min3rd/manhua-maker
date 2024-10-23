from translate import Translator
from modules.core.singleton import Singleton
import argostranslate.package
import argostranslate.translate
from deep_translator import GoogleTranslator

FOLDER_PATH_MODELS = "models"


class TranslateService(metaclass=Singleton):
    from_code: str
    to_code: str
    translator: Translator
    deep_translator: GoogleTranslator

    def __init__(self, from_code: str = "zh", to_code: str = "en"):
        self.from_code = from_code
        self.to_code = to_code
        self.translator = Translator(from_lang=from_code, to_lang=to_code)
        self.deep_translator = self.create_deep_translator(from_code, to_code)

    def translate(
        self,
        translator_engine: str,
        text: str,
        from_code: str = None,
        to_code: str = None,
    ) -> str:
        if translator_engine == "deep_translator":
            return self.deep_translate(text, from_code, to_code)
        elif translator_engine == "argostranslate":
            return self.argos_translate(text, from_code, to_code)
        elif translator_engine == "translate":
            return self.translate_translate(text, from_code, to_code)

    def argos_translate(
        self,
        text: str,
        from_code: str = None,
        to_code: str = None,
    ) -> str:
        if from_code is not None and to_code is not None:
            if self.from_code is not from_code or self.to_code is not to_code:
                self.from_code = from_code
                self.to_code = to_code
                argostranslate.package.install_from_path(
                    f"{FOLDER_PATH_MODELS}/{from_code}_{to_code}.argosmodel"
                )
        return argostranslate.translate.translate(text, from_code, to_code)

    def translate_translate(
        self, text: str, from_code: str = None, to_code: str = None
    ) -> str:
        if self.from_code is not from_code or self.to_code is not to_code:
            self.from_code = from_code
            self.to_code = to_code
            self.translator = Translator(from_lang=from_code, to_lang=to_code)
        return self.translator.translate(text)

    def create_deep_translator(self, from_code: str = None, to_code: str = None):
        if from_code == "zh":
            from_code = "zh-CN"
        return GoogleTranslator(source=from_code, target=to_code)

    def deep_translate(
        self, text: str, from_code: str = None, to_code: str = None
    ) -> str:
        if self.from_code is not from_code or self.to_code is not to_code:
            self.from_code = from_code
            self.to_code = to_code
            self.deep_translator = self.create_deep_translator(from_code, to_code)
        return self.deep_translator.translate(text)
