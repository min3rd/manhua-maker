from modules.core.singleton import Singleton
import os


class FileService(metaclass=Singleton):
    def __init__(self):
        pass

    def find_all_videos(self, path: str) -> list:
        print("Finding all videos")
        video_extensions = (".mp4", ".avi", ".mov", ".mkv")
        videos = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(video_extensions):
                    videos.append(os.path.join(root, file))
        return videos

    def get_file_name(self, file_path: str) -> str:
        return os.path.basename(file_path)

    def get_file_extension(self, file_path: str) -> str:
        return os.path.splitext(file_path)[1]

    def get_file_name_without_extension(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[0]
