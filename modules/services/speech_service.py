import json
import speech_recognition as sr

from modules.core.singleton import Singleton


class Word:
    word: str
    start: float
    end: float
    probability: float

    def __init__(self, entries):
        self.__dict__.update(entries)


class Segment:
    id: int
    seek: int
    start: float
    end: float
    text: str
    translated_text: str
    tokens: list[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float
    words: list[Word]
    audio_path: str = None

    def __init__(self, entries):
        self.__dict__.update(entries)


class SpeechRecognitionResult:
    text: str
    segments: list[Segment]
    language: str

    def __init__(self, entries):
        self.__dict__.update(entries)


class SpeechService(metaclass=Singleton):
    r = sr.Recognizer()

    def __init__(self):
        pass

    def recognite(
        self,
        audio_path: str,
        model: str = "base",
        language: str = "zh",
        translate: bool = False,
        show_dict: bool = False,
    ) -> SpeechRecognitionResult:
        print("Recognizing speech")
        with sr.AudioFile(audio_path) as source:
            audio = self.r.record(source)
        return json.loads(
            json.dumps(
                self.r.recognize_whisper(
                    audio,
                    model=model,
                    language=language,
                    translate=translate,
                    word_timestamps=True,
                    show_dict=show_dict,
                )
            ),
            object_hook=SpeechRecognitionResult,
        )
