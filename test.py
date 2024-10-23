import json
from modules.services.audio_service import AudioService
from modules.services.json_service import JsonService
from modules.services.speech_service import SpeechRecognitionResult
from modules.services.translate_service import TranslateService
from modules.services.tts_service import TTSService

filename = "Jiang-17"
from_code = "zh"
to_code = "en"
translate_service = TranslateService()
audio_service = AudioService()
json_service = JsonService()
tts_service = TTSService()
json_string = json_service.get_json_string_from_file(f"json/{filename}.json")
data: SpeechRecognitionResult = json.loads(
    json_string,
    object_hook=SpeechRecognitionResult,
)

for segment in data.segments:
    print(f"Translating segment {segment.id}")
    translated_text = translate_service.argos_translate(
        text=segment.text, from_code=from_code, to_code=to_code
    )
    if not translated_text or len(translated_text) <= 0:
        data.segments.remove(segment)
        continue
    print(f"Saving audio for segment {segment.id} with text: {translated_text}")
    segment_audio_path = f"audios/{segment.id}.mp3"
    tts_service.to_file(translated_text, segment_audio_path, lang=to_code)
    segment.audio_path = segment_audio_path
    segment.translated_text = translated_text
try:
    json_service.to_file(data, f"json/{filename}.json")
except Exception as e:
    print(f"Error saving json: {e}")

audio_service.composite(
    f"videos/{filename}.mp4",
    f"audios/{filename}.wav",
    data.segments,
    f"export/{filename}_final.mp4",
)
