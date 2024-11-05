import json
import os
import shutil
from modules.services.audio_service import AudioService
from modules.services.file_service import FileService
from modules.services.json_service import JsonService
from modules.services.speech_service import SpeechService
from modules.services.translate_service import TranslateService
from modules.services.tts_service import TTSService
from modules.services.video_service import VideoService
from modules.services.word_service import WordService
import inquirer

FOLDER_PATH_AUDIOS = "audios"
FOLDER_PATH_JSON = "json"
FOLDER_PATH_DONE = "done"
FOLDER_PATH_EXPORT = "export"
FOLDER_PATH_VIDEOS = "videos"
FOLDER_PATH_BACKUP = "backup"
FOLDER_PATH_BACKUP_EXPORT = FOLDER_PATH_BACKUP + "/0." + FOLDER_PATH_EXPORT
FILE_PATH_CONFIG = "config.json"
DATA_FOLDERS = [FOLDER_PATH_AUDIOS, FOLDER_PATH_JSON]
COMPLETED_FOLDER = [
    FOLDER_PATH_DONE,
    FOLDER_PATH_EXPORT,
    FOLDER_PATH_BACKUP,
    FOLDER_PATH_BACKUP_EXPORT,
]
MENU_TRANSLATE_VIDEO = "Translate video"
MENU_TRANSLATE_ALL_VIDEO = "Translate all video"
MENU_SPLIT_VIDEO = "Split video"
MENU_UPLOAD = "Upload"
MENU_SETTINGS = "Settings"
MENU_EXIT = "Exit"
MENU_BACKUP = "Backup"
MENU_OPEN_VIDEOS_FOLDER = "Open videos folder"
MENU_OPEN_EXPORT_FOLDER = "Open export folder"

SETTINGS_LANG_CODE_ZH = "zh"
SETTINGS_LANG_CODE_EN = "en"
SETTINGS_LANG_CODE_IN = "in"
SETTINGS_LANG_CODE_JA = "ja"
SETTINGS_LANG_CODE_KO = "ko"
SETTINGS_LANG_CODE_FR = "fr"
SETTINGS_LANG_CODE_DE = "de"
SETTINGS_LANG_CODE_ES = "es"
SETTINGS_LANG_CODE_IT = "it"
SETTINGS_LANG_CODE_NL = "nl"
SETTINGS_LANG_CODE_PT = "pt"
SETTINGS_LANG_CODE_RU = "ru"
SETTINGS_LANG_CODE_AR = "ar"
SETTINGS_LANG_CODE_TR = "tr"
SETTINGS_LANG_CODE_VI = "vi"
SETTINGS_LANG_CODE_TH = "th"

SETTINGS_VIDEO_LENGTH_3 = 3
SETTINGS_VIDEO_LENGTH_5 = 5
SETTINGS_VIDEO_LENGTH_10 = 10
SETTINGS_VIDEO_LENGTH_15 = 15
SETTINGS_SPEECH_RATE_125 = 125
SETTINGS_SPEECH_RATE_150 = 150
SETTINGS_SPEECH_RATE_175 = 175
SETTINGS_SPEECH_RATE_200 = 200
SETTINGS_TRANSLATOR_ENGINE_DEEP_TRANSLATOR = "deep_translator"
SETTINGS_TRANSLATOR_ENGINE_ARGOSTRANSLATE = "argostranslate"
SETTINGS_TRANSLATOR_ENGINE_TRANSLATE = "translate"
SETTINGS_TTS_ENGINE_PYTTSX3 = "pyttsx3"
SETTINGS_TTS_ENGINE_GTTS = "gtts"
SETTINGS_BACKGROUND_VOLUME_0 = 0
SETTINGS_BACKGROUND_VOLUME_10 = 0.1
SETTINGS_BACKGROUND_VOLUME_20 = 0.2
SETTINGS_BACKGROUND_VOLUME_30 = 0.3
SETTINGS_BACKGROUND_VOLUME_50 = 0.5
SETTINGS_BACKGROUND_VOLUME_60 = 0.6
SETTINGS_BACKGROUND_VOLUME_70 = 0.7
SETTINGS_BACKGROUND_VOLUME_80 = 0.8
SETTINGS_BACKGROUND_VOLUME_90 = 0.9
SETTINGS_BACKGROUND_VOLUME_100 = 1
SETTINGS_VIDEO_SCALE_0 = 0
SETTINGS_VIDEO_SCALE_10 = 0.1
SETTINGS_VIDEO_SCALE_20 = 0.2
SETTINGS_VIDEO_SCALE_30 = 0.3
SETTINGS_VIDEO_SCALE_40 = 0.4
SETTINGS_VIDEO_SCALE_50 = 0.5
SETTINGS_VIDEO_SCALE_60 = 0.6
SETTINGS_VIDEO_SCALE_70 = 0.7
SETTINGS_VIDEO_SCALE_80 = 0.8
SETTINGS_VIDEO_SCALE_90 = 0.9
SETTINGS_VIDEO_SCALE_100 = 1

SETTINGS_VIDEO_QUALITY_360 = 360
SETTINGS_VIDEO_QUALITY_480 = 480
SETTINGS_VIDEO_QUALITY_720 = 720
SETTINGS_VIDEO_QUALITY_1080 = 1080


class Config:
    from_code: str = SETTINGS_LANG_CODE_ZH
    to_code: str = SETTINGS_LANG_CODE_EN
    video_length: int = SETTINGS_VIDEO_LENGTH_10
    speech_rate: int = SETTINGS_SPEECH_RATE_175
    done: list[str] = []
    translator_engine: str = SETTINGS_TRANSLATOR_ENGINE_DEEP_TRANSLATOR
    tts_engine: str = SETTINGS_TTS_ENGINE_PYTTSX3
    background_volume: int = SETTINGS_BACKGROUND_VOLUME_0
    video_scale: int = SETTINGS_VIDEO_SCALE_70
    video_quality: int = SETTINGS_VIDEO_QUALITY_1080

    def __init__(
        self,
        from_code: str,
        to_code: str,
        video_length: int,
        speech_rate: float,
        done: list[str] = [],
        translator_engine: str = SETTINGS_TRANSLATOR_ENGINE_DEEP_TRANSLATOR,
        tts_engine: str = SETTINGS_TTS_ENGINE_PYTTSX3,
        background_volume: int = SETTINGS_BACKGROUND_VOLUME_0,
        video_scale: int = SETTINGS_VIDEO_SCALE_0,
        video_quality: int = SETTINGS_VIDEO_QUALITY_1080,
    ):
        self.from_code = from_code
        self.to_code = to_code
        self.video_length = video_length
        self.speech_rate = speech_rate
        self.done = done
        self.translator_engine = translator_engine
        self.tts_engine = tts_engine
        self.background_volume = background_volume
        self.video_scale = video_scale
        self.video_quality = video_quality


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
        if MENU_BACKUP == answer["menu"]:
            self.backup()
        if MENU_OPEN_VIDEOS_FOLDER == answer["menu"]:
            self.open_videos_folder()
        if MENU_OPEN_EXPORT_FOLDER == answer["menu"]:
            self.open_export_folder()
        self.run()

    def menu(self, choices=list[str]) -> str:
        return inquirer.prompt(
            [
                inquirer.List(
                    "menu",
                    "Select the options you want to run",
                    choices=choices,
                    carousel=True,
                ),
            ]
        )

    def menu_main(self):
        return self.menu(
            [
                MENU_TRANSLATE_VIDEO,
                MENU_TRANSLATE_ALL_VIDEO,
                MENU_SPLIT_VIDEO,
                MENU_OPEN_VIDEOS_FOLDER,
                MENU_OPEN_EXPORT_FOLDER,
                MENU_BACKUP,
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
            self.tts_service.to_file(
                engine=self.config.tts_engine,
                text=translated_text,
                file_path=segment_audio_path,
                lang=self.config.to_code,
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
        width = 1920
        height = 1080
        word_limit = 10
        if self.config.video_quality == SETTINGS_VIDEO_QUALITY_360:
            width = 640
            height = 360
            word_limit = 5
        if self.config.video_quality == SETTINGS_VIDEO_QUALITY_480:
            width = 854
            height = 480
            word_limit = 5
        if self.config.video_quality == SETTINGS_VIDEO_QUALITY_720:
            width = 1280
            height = 720
            word_limit = 7
        if self.config.video_quality == SETTINGS_VIDEO_QUALITY_1080:
            width = 1920
            height = 1080
            word_limit = 10
        if self.audio_service.composite(
            video_path,
            audio_path,
            data.segments,
            final_audio_path,
            word_limit=word_limit,
            video_zoom_factor=self.config.video_scale,
            width=width,
            height=height,
            background_volume=self.config.background_volume,
        ):
            self.save_video_state(video_path)
            # sleep(10)
            # self.file_service.copy(
            #     video_path, f"{FOLDER_PATH_DONE}/{file_name_without_extension}.mp4"
            # )
        return True

    def upload(self):
        pass

    def settings(self):
        old_done = self.config.done
        answers = inquirer.prompt(
            [
                inquirer.List(
                    "from_code",
                    message="Enter the code of the original language",
                    choices=[
                        SETTINGS_LANG_CODE_ZH,
                        SETTINGS_LANG_CODE_EN,
                        SETTINGS_LANG_CODE_IN,
                        SETTINGS_LANG_CODE_JA,
                        SETTINGS_LANG_CODE_KO,
                        SETTINGS_LANG_CODE_FR,
                        SETTINGS_LANG_CODE_DE,
                        SETTINGS_LANG_CODE_ES,
                        SETTINGS_LANG_CODE_IT,
                        SETTINGS_LANG_CODE_NL,
                        SETTINGS_LANG_CODE_PT,
                        SETTINGS_LANG_CODE_RU,
                        SETTINGS_LANG_CODE_AR,
                        SETTINGS_LANG_CODE_TR,
                        SETTINGS_LANG_CODE_VI,
                        SETTINGS_LANG_CODE_TH,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "to_code",
                    message="Enter the code of the target language",
                    choices=[
                        SETTINGS_LANG_CODE_ZH,
                        SETTINGS_LANG_CODE_EN,
                        SETTINGS_LANG_CODE_IN,
                        SETTINGS_LANG_CODE_JA,
                        SETTINGS_LANG_CODE_KO,
                        SETTINGS_LANG_CODE_FR,
                        SETTINGS_LANG_CODE_DE,
                        SETTINGS_LANG_CODE_ES,
                        SETTINGS_LANG_CODE_IT,
                        SETTINGS_LANG_CODE_NL,
                        SETTINGS_LANG_CODE_PT,
                        SETTINGS_LANG_CODE_RU,
                        SETTINGS_LANG_CODE_AR,
                        SETTINGS_LANG_CODE_TR,
                        SETTINGS_LANG_CODE_VI,
                        SETTINGS_LANG_CODE_TH,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "video_length",
                    message="Enter the length of the video (minutes)",
                    choices=[
                        SETTINGS_VIDEO_LENGTH_3,
                        SETTINGS_VIDEO_LENGTH_5,
                        SETTINGS_VIDEO_LENGTH_10,
                        SETTINGS_VIDEO_LENGTH_15,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "speech_rate",
                    message="Enter the speech rate",
                    choices=[
                        SETTINGS_SPEECH_RATE_125,
                        SETTINGS_SPEECH_RATE_150,
                        SETTINGS_SPEECH_RATE_175,
                        SETTINGS_SPEECH_RATE_200,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "translator_engine",
                    message="Enter the translator engine",
                    choices=[
                        SETTINGS_TRANSLATOR_ENGINE_DEEP_TRANSLATOR,
                        SETTINGS_TRANSLATOR_ENGINE_ARGOSTRANSLATE,
                        SETTINGS_TRANSLATOR_ENGINE_TRANSLATE,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "tts_engine",
                    message="Enter the TTS engine",
                    choices=[SETTINGS_TTS_ENGINE_PYTTSX3, SETTINGS_TTS_ENGINE_GTTS],
                ),
                inquirer.List(
                    "background_volume",
                    message="Enter the background volume",
                    choices=[
                        SETTINGS_BACKGROUND_VOLUME_0,
                        SETTINGS_BACKGROUND_VOLUME_10,
                        SETTINGS_BACKGROUND_VOLUME_20,
                        SETTINGS_BACKGROUND_VOLUME_30,
                        SETTINGS_BACKGROUND_VOLUME_50,
                        SETTINGS_BACKGROUND_VOLUME_60,
                        SETTINGS_BACKGROUND_VOLUME_70,
                        SETTINGS_BACKGROUND_VOLUME_80,
                        SETTINGS_BACKGROUND_VOLUME_90,
                        SETTINGS_BACKGROUND_VOLUME_100,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "video_scale",
                    message="Enter the video scale: (default is 100%)",
                    choices=[
                        SETTINGS_VIDEO_SCALE_0,
                        SETTINGS_VIDEO_SCALE_10,
                        SETTINGS_VIDEO_SCALE_20,
                        SETTINGS_VIDEO_SCALE_30,
                        SETTINGS_VIDEO_SCALE_40,
                        SETTINGS_VIDEO_SCALE_50,
                        SETTINGS_VIDEO_SCALE_60,
                        SETTINGS_VIDEO_SCALE_70,
                        SETTINGS_VIDEO_SCALE_80,
                        SETTINGS_VIDEO_SCALE_90,
                        SETTINGS_VIDEO_SCALE_100,
                    ],
                    carousel=True,
                ),
                inquirer.List(
                    "video_quality",
                    message="Enter the video quality",
                    choices=[
                        SETTINGS_VIDEO_QUALITY_360,
                        SETTINGS_VIDEO_QUALITY_480,
                        SETTINGS_VIDEO_QUALITY_720,
                        SETTINGS_VIDEO_QUALITY_1080,
                    ],
                    carousel=True,
                ),
            ]
        )
        self.config.from_code = answers["from_code"]
        self.config.to_code = answers["to_code"]
        self.config.video_length = answers["video_length"]
        self.config.speech_rate = answers["speech_rate"]
        self.config.translator_engine = answers["translator_engine"]
        self.config.tts_engine = answers["tts_engine"]
        self.config.background_volume = answers["background_volume"]
        self.config.video_scale = answers["video_scale"]
        self.config.video_quality = answers["video_quality"]
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

    def backup(self):
        self.file_service.move(FOLDER_PATH_VIDEOS, FOLDER_PATH_BACKUP)
        self.file_service.move(FOLDER_PATH_EXPORT, FOLDER_PATH_BACKUP_EXPORT)
        os.makedirs(FOLDER_PATH_VIDEOS, exist_ok=True)
        os.makedirs(FOLDER_PATH_EXPORT, exist_ok=True)
        self.config.done = []
        self.json_service.to_file(self.config, FILE_PATH_CONFIG)

    def open_videos_folder(self):
        self.file_service.open_folder(FOLDER_PATH_VIDEOS)

    def open_export_folder(self):
        self.file_service.open_folder(FOLDER_PATH_EXPORT)
