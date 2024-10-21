import os
import shutil
from time import sleep
from modules.services.audio_service import AudioService
from modules.services.file_service import FileService
from modules.services.json_service import JsonService
from modules.services.speech_service import SpeechService
from modules.services.translate_service import TranslateService
from modules.services.tts_service import TTSService
from modules.services.video_service import VideoService
from modules.services.word_service import WordService


class Main:
    video_service = VideoService()
    speech_service = SpeechService()
    translate_service = TranslateService()
    word_service = WordService()
    tts_service = TTSService()
    file_service = FileService()
    audio_service = AudioService()
    json_service = JsonService()

    def __init__(self):
        pass

    def run(self, from_code: str = "zh", to_code: str = "en"):
        print("Running main")
        shutil.rmtree("audios", ignore_errors=True)
        shutil.rmtree("json", ignore_errors=True)
        os.makedirs("audios", exist_ok=True)
        os.makedirs("export", exist_ok=True)
        os.makedirs("json", exist_ok=True)
        os.makedirs("done", exist_ok=True)

        video_paths = self.file_service.find_all_videos("videos")
        for video_path in video_paths:
            print(f"Processing video {video_path}")

            file_name_without_extension = (
                self.file_service.get_file_name_without_extension(video_path)
            )
            audio_path = f"audios/{file_name_without_extension}.wav"
            self.video_service.get_audio(
                video_path=video_path,
                output_path=audio_path,
            )
            try:
                data = self.speech_service.recognite(
                    audio_path, language=from_code, translate=False, show_dict=True
                )
            except Exception as e:
                print(f"Error recognizing speech: {e}")
                continue
            for segment in data.segments:
                translated_text = self.translate_service.argostranslate(
                    text=segment.text, from_code=from_code, to_code=to_code
                )
                if not translated_text or len(translated_text) <= 0:
                    data.segments.remove(segment)
                    continue
                segment_audio_path = f"audios/{segment.id}.mp3"
                self.tts_service.to_file(
                    translated_text, segment_audio_path, lang=to_code, speech_rate=175
                )
                segment.audio_path = segment_audio_path
                segment.translated_text = translated_text
            try:
                self.json_service.to_file(
                    data, f"json/{file_name_without_extension}.json"
                )
            except Exception as e:
                print(f"Error saving json: {e}")
            final_audio_path = f"export/{file_name_without_extension}_final.mp4"
            if self.audio_service.composite(
                video_path, audio_path, data.segments, final_audio_path
            ):
                sleep(10)
                self.file_service.move(
                    video_path, f"done/{file_name_without_extension}.mp4"
                )
