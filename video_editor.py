import time
import math
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip
from faster_whisper import WhisperModel

def combine_sound_and_video(video_path, audio_path, output_path):
  video = VideoFileClip(video_path)
  audio = AudioFileClip(audio_path)

  video = video.set_audio(audio)
  video.write_videofile(output_path, codec='libx264', audio_codec='aac')

def add_subtitles(input_path, audio_path, output_path):
  input_video_name = input_path.replace(".mp4", "")

def transcribe(audio):
    model = WhisperModel("small", device="cuda", compute_type="float32")
    segments, info = model.transcribe(audio)
    language = info[0]
    print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments

# # Example usage
# video_path = './stock videos/minecraft.mp4'
# audio_path = './speech.mp3'
# output_path = './output/tiktok.mp4'

# combine_sound_and_video(video_path, audio_path, output_path)

transcribe('./speech.mp3')