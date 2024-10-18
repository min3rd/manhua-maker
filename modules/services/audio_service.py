from modules.core.singleton import Singleton
from modules.services.speech_service import Segment
import moviepy.editor as mp
import moviepy.audio.fx.all as afx
import moviepy.video.fx.all as vfx
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings

change_settings(
    {"IMAGEMAGICK_BINARY": r"libs/ImageMagick-7.1.1-39-portable-Q16-x64/magick.exe"}
)


class AudioService(metaclass=Singleton):
    def __init__(self):
        pass

    def composite(
        self,
        video_path: str,
        background_audio_path: str,
        segments: list[Segment],
        output_path: str,
        word_limit: int = 5,
    ):
        print("Concatenating audios")
        video = mp.VideoFileClip(video_path)
        background_audio = mp.AudioFileClip(background_audio_path)
        last_end = 0
        video_clips = []
        audio_clips = []
        subtitles = []
        for segment in segments:
            try:
                print(f"Adding segment {segment.audio_path}")
                if segment.start > last_end:
                    no_translate_audio = background_audio.subclip(
                        last_end, segment.start
                    )
                    video_clips.append(video.subclip(last_end, segment.start))
                    audio_clips.append(no_translate_audio)
                segment_audio = mp.AudioFileClip(segment.audio_path)
                background_audio_clip = background_audio.subclip(
                    segment.start, segment.end
                )
                background_audio_clip = background_audio_clip.fx(
                    vfx.speedx, background_audio_clip.duration / segment_audio.duration
                )
                background_audio_clip = afx.volumex(background_audio_clip, 0.1)
                composite_audio = mp.CompositeAudioClip(
                    [background_audio_clip, segment_audio]
                )
                current_audio_duration: int = sum(
                    [clip.duration for clip in audio_clips]
                )
                words = segment.translated_text.split(" ")
                appear_time = composite_audio.duration / len(words)
                start_time = current_audio_duration
                line = []
                for word_index, word in enumerate(words):
                    if len(line) > word_limit:
                        line.remove(line[0])
                    line.append(word)
                    subtitles.append(
                        (
                            (
                                start_time + appear_time * word_index,
                                start_time + appear_time * (word_index + 1),
                            ),
                            " ".join(line),
                        )
                    )
                audio_clips.append(composite_audio)
                real_duration = segment.end - segment.start
                audio_duration = segment_audio.duration
                video_speed = real_duration / audio_duration
                video_clip = video.subclip(segment.start, segment.end)
                video_clip = video_clip.fx(vfx.speedx, video_speed)
                video_clips.append(video_clip)
            except Exception as e:
                print(f"Error processing segment {segment.id}: {e}")
                no_translate_audio = background_audio.subclip(last_end, segment.start)
                video_clips.append(video.subclip(last_end, segment.start))
                audio_clips.append(no_translate_audio)
            last_end = segment.end
        video = mp.concatenate_videoclips(video_clips)
        final_audio = mp.concatenate_audioclips(audio_clips)
        video = video.set_audio(final_audio)
        subtitle_clip = SubtitlesClip(
            subtitles,
            lambda txt: mp.TextClip(
                txt,
                font="Arial",
                fontsize=56,
                color="white",
                bg_color="black",
            ),
        )
        video = mp.CompositeVideoClip(
            [video, subtitle_clip.set_position(("center", "bottom"))]
        )
        video.write_videofile(output_path, codec="libx264")

    def copy(self, audio_path: str, output_path: str):
        print("Copying audio")
        audio = mp.AudioFileClip(audio_path)
        audio.write_audiofile(output_path, fps=audio.fps)
