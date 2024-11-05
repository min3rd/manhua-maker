from modules.services.video_service import VideoService
from moviepy.editor import VideoFileClip

video_service = VideoService()
clip = VideoFileClip("raw.mp4")
video_service.zoom_in_center(
    clip=clip, scale_factor=0.6, output_path="output.mp4", width=640, height=360
)
