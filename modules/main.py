import json
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
import inquirer

from modules.services.youtube_service import YoutubeService

FOLDER_PATH_AUDIOS = "audios"
FOLDER_PATH_JSON = "json"
FOLDER_PATH_DONE = "done"
FOLDER_PATH_EXPORT = "export"
FOLDER_PATH_VIDEOS = "videos"
FILE_PATH_CONFIG = "config.json"
DATA_FOLDERS = [FOLDER_PATH_AUDIOS, FOLDER_PATH_JSON]
COMPLETED_FOLDER = [FOLDER_PATH_DONE, FOLDER_PATH_EXPORT]
MENU_TRANSLATE_VIDEO = "Translate video"
MENU_TRANSLATE_ALL_VIDEO = "Translate all video"
MENU_SPLIT_VIDEO = "Split video"
MENU_UPLOAD = "Upload"
MENU_SETTINGS = "Settings"
MENU_EXIT = "Exit"


class Config:
    from_code: str = "zh"
    to_code: str = "en"
    video_length: int = 10
    speech_rate: int = 175
    done: list[str] = []
    translator_engine: str = "deep_translator"

    def __init__(
        self,
        from_code: str,
        to_code: str,
        video_length: int,
        speech_rate: float,
        done: list[str] = [],
        translator_engine: str = "deep_translator",
    ):
        self.from_code = from_code
        self.to_code = to_code
        self.video_length = video_length
        self.speech_rate = speech_rate
        self.done = done
        self.translator_engine = translator_engine


class Main:
    config: Config
    video_service = VideoService()
    speech_service = SpeechService()
    translate_service = TranslateService()
    word_service = WordService()
    tts_service = TTSService()
    file_service = FileService()
    audio_service = AudioService()
    json_service = JsonService()
    youtube_service = YoutubeService()
    youtube = None

    def __init__(self):
        try:
            self.config = json.loads(
                self.json_service.get_json_string_from_file(FILE_PATH_CONFIG),
                object_hook=lambda d: Config(**d),
            )
        except FileNotFoundError:
            self.config = Config("zh", "en", 10, 175)

    def run(self):
        answer = self.menu_main()
        if MENU_TRANSLATE_ALL_VIDEO == answer["menu"]:
            self.make_all_video(self.config.from_code, self.config.to_code)
        if MENU_SPLIT_VIDEO == answer["menu"]:
            self.split_video(self.config.video_length)
        if MENU_UPLOAD == answer["menu"]:
            print("Uploading")
            self.upload()
        if MENU_SETTINGS == answer["menu"]:
            print(MENU_SETTINGS)
            self.settings()
        if MENU_EXIT == answer["menu"]:
            print("Exiting")
            return
        if MENU_TRANSLATE_VIDEO == answer["menu"]:
            self.translate_video()
        self.run()

    def menu(self, choices=list[str]) -> str:
        return inquirer.prompt(
            [
                inquirer.List(
                    "menu",
                    "Select the options you want to run",
                    choices=choices,
                ),
            ]
        )

    def menu_main(self):
        return self.menu(
            [
                MENU_TRANSLATE_VIDEO,
                MENU_TRANSLATE_ALL_VIDEO,
                MENU_SPLIT_VIDEO,
                MENU_SETTINGS,
                MENU_EXIT,
            ]
        )

    def menu_upload(self, video_paths: list[str]):
        return self.menu(video_paths)

    def renew_folders(self):
        for folder in DATA_FOLDERS:
            shutil.rmtree(folder, ignore_errors=True)
            os.makedirs(folder, exist_ok=True)
        for folder in COMPLETED_FOLDER:
            os.makedirs(folder, exist_ok=True)

    def make_all_video(self, from_code: str = None, to_code: str = None):
        if from_code is not None:
            self.config.from_code = from_code
        if to_code is not None:
            self.config.to_code = to_code
        self.renew_folders()
        video_paths = self.file_service.find_all_videos(FOLDER_PATH_VIDEOS)
        for video_path in video_paths:
            print(f"Processing video {video_path}")
            if self.config.done and video_path in self.config.done:
                print("Video already processed, skipping")
                continue
            if self.video_service.get_video_duration(video_path) > (
                self.config.video_length * 60 + 1
            ):
                print("Video is too long to process, skipping")
                continue
            self.make_video(video_path, self.config.from_code, self.config.to_code)

    def make_video(self, video_path: str, from_code: str = None, to_code: str = None):
        shutil.rmtree(FOLDER_PATH_AUDIOS, ignore_errors=True)
        os.makedirs(FOLDER_PATH_AUDIOS, exist_ok=True)
        if from_code is not None:
            self.config.from_code = from_code
        if to_code is not None:
            self.config.to_code = to_code
        file_name_without_extension = self.file_service.get_file_name_without_extension(
            video_path
        )
        audio_path = f"{FOLDER_PATH_AUDIOS}/{file_name_without_extension}.wav"
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
            return False
        for segment in data.segments:
            translated_text = self.translate_service.translate(
                translator_engine=self.config.translator_engine,
                text=segment.text,
                from_code=self.config.from_code,
                to_code=self.config.to_code,
            )
            if not translated_text or len(translated_text) <= 0:
                translated_text = segment.text
            segment_audio_path = f"{FOLDER_PATH_AUDIOS}/{segment.id}.mp3"
            self.tts_service.pyttsx3_to_file(
                translated_text,
                segment_audio_path,
                lang=to_code,
                speech_rate=self.config.speech_rate,
            )
            segment.audio_path = segment_audio_path
            segment.translated_text = translated_text
        try:
            self.json_service.to_file(
                data, f"{FOLDER_PATH_JSON}/{file_name_without_extension}.json"
            )
        except Exception as e:
            print(f"Error saving json: {e}")
        final_audio_path = (
            f"{FOLDER_PATH_EXPORT}/{file_name_without_extension}_final.mp4"
        )
        if self.audio_service.composite(
            video_path, audio_path, data.segments, final_audio_path, word_limit=10
        ):
            self.save_video_state(video_path)
            # sleep(10)
            # self.file_service.copy(
            #     video_path, f"{FOLDER_PATH_DONE}/{file_name_without_extension}.mp4"
            # )
        return True

    def upload(self):
        if not self.youtube:
            self.youtube = self.youtube_service.authenticate_youtube()

    def settings(self):
        old_done = self.config.done
        self.config = inquirer.prompt(
            [
                inquirer.List(
                    "from_code",
                    message="Enter the code of the original language",
                    choices=["zh", "en"],
                ),
                inquirer.List(
                    "to_code",
                    message="Enter the code of the target language",
                    choices=["zh", "en"],
                ),
                inquirer.List(
                    "video_length",
                    message="Enter the length of the video (minutes)",
                    choices=[3, 5, 10, 15],
                ),
                inquirer.List(
                    "speech_rate",
                    message="Enter the speech rate",
                    choices=[125, 150, 175, 200],
                ), 
                inquirer.List(
                    "translator_engine",
                    message="Enter the translator engine",
                    choices=["deep_translator", "argostranslate", "translate"],
                ),
            ]
        )
        self.config.done = old_done
        self.json_service.to_file(self.config, FILE_PATH_CONFIG)

    def split_video(self, video_length: int = None):
        if video_length is not None:
            self.config.video_length = video_length
        video_paths = self.file_service.find_all_videos(FOLDER_PATH_VIDEOS)
        for video_path in video_paths:
            print(f"Processing video {video_path}")
            self.video_service.split_video(video_path, self.config.video_length)

    def save_video_state(self, video_path: str):
        self.config.done.append(video_path)
        self.json_service.to_file(self.config, FILE_PATH_CONFIG)

    def reset_video_state(self):
        self.config.done = []
        self.json_service.to_file(self.config, FILE_PATH_CONFIG)

    def save_config(self):
        self.json_service.to_file(self.config, FILE_PATH_CONFIG)

    def translate_video(self):
        video_paths = self.file_service.find_all_videos(FOLDER_PATH_VIDEOS)
        answer = inquirer.prompt(
            [
                inquirer.List(
                    "video_path",
                    message="Select the video you want to translate",
                    choices=video_paths,
                ),
            ]
        )
        video_path = answer["video_path"]
        self.make_video(video_path, self.config.from_code, self.config.to_code)
