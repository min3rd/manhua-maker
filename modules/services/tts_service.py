from modules.core.singleton import Singleton
import pyttsx3
from gtts import gTTS


class TTSService(metaclass=Singleton):
    use_gtts = False
    engine = None

    def __init__(self):
        self.init()

    def to_file(
        self,
        engine: str,
        text: str,
        file_path: str,
        lang: str = "en",
        tld: str = "com",
        speech_rate: int = 225,
    ) -> bool:
        if engine == "gtts":
            return self.gtts_to_file(text, file_path, lang, tld)
        if engine == "pyttsx3":
            return self.pyttsx3_to_file(text, file_path, lang, speech_rate)

    def gtts_to_file(
        self,
        text: str,
        file_path: str,
        lang: str = "en",
        tld: str = "com",
    ) -> bool:
        try:

            tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
            tts.save(file_path)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def pyttsx3_to_file(
        self, text: str, file_path: str, lang: str = "en", speech_rate: int = 225
    ) -> bool:
        try:
            if not self.engine:
                self.init(speech_rate=speech_rate)
            self.engine.setProperty("rate", speech_rate)
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def init(self, speech_rate: int = 225):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", speech_rate)
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if f"{voice.name}".find("Zira") != -1:
                self.engine.setProperty("voice", voice.id)
                break
