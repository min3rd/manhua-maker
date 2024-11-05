import moviepy.editor as mp
from moviepy.video.VideoClip import VideoClip
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

    def zoom_in_center(
        self,
        clip: VideoClip,
        scale_factor: float,
        width: float = None,
        height: float = None,
        output_path: str = None,
    ):
        resize_width = clip.w * scale_factor
        resize_height = clip.h * scale_factor
        zoomed_clip = self.crop_video_center(clip, resize_width, resize_height)
        if width is None and height is None:
            width = clip.w
            height = clip.h
        resize = self.resize_video(zoomed_clip, width=width, height=height)
        if output_path:
            resize.write_videofile(output_path, codec="libx264")
        return resize

    def crop_video_center(
        self, clip: VideoClip, width, height, output_path: str = None
    ):
        x_center = (clip.w - width) / 2
        y_center = (clip.h - height) / 2
        cropped_clip = clip.crop(
            x_center, y_center, x_center + width, y_center + height
        )
        if output_path:
            cropped_clip.write_videofile(output_path, codec="libx264")
        return cropped_clip

    def resize_video(
        self, clip: VideoClip, width: int, height: int, output_path: str = None
    ):
        resized_clip = clip.fx(mp.vfx.resize, width=width, height=height)
        if output_path:
            resized_clip.write_videofile(output_path, codec="libx264")
        return resized_clip
