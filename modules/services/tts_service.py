from modules.core.singleton import Singleton
from gtts import gTTS
import pyttsx3


class TTSService(metaclass=Singleton):
    use_gtts = False
    engine = None

    def __init__(self):
        self.init()

    def to_file(self, text: str, file_path: str, lang: str = "en", tld: str = "us"):
        if self.use_gtts:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(file_path)
        else:
            if not self.engine:
                self.init()
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()

    def init(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 250)
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if f"{voice.name}".find("Zira") != -1:
                self.engine.setProperty("voice", voice.id)
                break
