from modules.core.singleton import Singleton
from gtts import gTTS
import pyttsx3


class TTSService(metaclass=Singleton):
    use_gtts = False
    engine = pyttsx3.init()

    def __init__(self):
        self.engine.setProperty("rate", 125)

    def to_file(self, text: str, file_path: str, lang: str = "en", tld: str = "us"):
        if self.use_gtts:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(file_path)
        else:
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()
