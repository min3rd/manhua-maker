import moviepy.editor as mp

from modules.core.singleton import Singleton


class VideoService(metaclass=Singleton):
    def __init__(self):
        pass

    def play(self, video_path: str):
        print(f"Playing video {video_path}")

    def get_audio(self, video_path: str, output_path: str = None):
        print("Getting audio from video")

        video = mp.VideoFileClip(video_path)
        audio = video.audio
        if output_path:
            audio.write_audiofile(output_path)
        else:
            return audio
