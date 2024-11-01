import moviepy.editor as mp

from modules.core.singleton import Singleton
from modules.services.file_service import FileService


class VideoService(metaclass=Singleton):
    file_service = FileService()

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

    def split_video(self, video_path: str, limit: int = 10):
        print(f"Splitting video {video_path}")
        split_video_duration = limit * 60  # limit in minutes to seconds
        video = mp.VideoFileClip(video_path)
        duration = video.duration
        if duration < split_video_duration:
            return
        filename = self.file_service.get_file_name_without_extension(video_path)
        folder_path = self.file_service.get_folder_path(video_path)
        ep_number = 1
        current_position = 0
        while current_position < duration:
            try:
                end = current_position + split_video_duration
                if end > duration:
                    end = duration
                if end + split_video_duration / 2 > duration:
                    end = duration
                clip = video.subclip(current_position, end)
                clip.write_videofile(
                    f"{folder_path}/" + "{:03}".format(ep_number) + f"_{filename}.mp4"
                )
                ep_number += 1
                current_position += split_video_duration
            except Exception as e:
                print(f"Error splitting video: {e}")

    def get_video_duration(self, video_path: str):
        video = mp.VideoFileClip(video_path)
        return video.duration  # in seconds
