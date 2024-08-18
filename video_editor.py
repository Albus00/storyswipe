import time
import math
# import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from faster_whisper import WhisperModel
from moviepy.config import change_settings

SUBTITLE_FILE_NAME = "subtitles.srt"

# Change this to the path of your ImageMagick installation (autodetection doesn't work)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def combine_sound_and_video(video_path, audio_path, output_path):
  video = VideoFileClip(video_path)
  audio = AudioFileClip(audio_path)

  video = video.set_audio(audio)
  video.write_videofile(output_path, codec='libx264', audio_codec='aac')

def add_subtitles(input_path, audio_path, output_path):
  # Followed this guide: https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg
  # Used this to get faster whisper working: https://stackoverflow.com/questions/66355477/could-not-load-library-cudnn-ops-infer64-8-dll-error-code-126-please-make-sure
  
  segments = transcribe(audio_path)
  print("Transcription - complete")
  generate_subtitle_file(segments)
  print("Subtitle file - created")

#   render_subtitle_to_video(input_path, output_path)


def transcribe(audio):
    model = WhisperModel("small", device="cuda", compute_type="float32")
    segments, _ = model.transcribe(audio, language='en')
    segments = list(segments)
    return segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(segments, input_video_name="video"):

    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"

    # Save subtitle file
    with open(SUBTITLE_FILE_NAME, "w") as f:
        f.write(text)

def render_subtitle_to_video(input_path, output_path):
    # https://superuser.com/questions/874598/creating-video-containing-animated-text-using-ffmpeg-alone/874697#874697

    generator = lambda txt: TextClip(txt, font='Georgia-Regular', fontsize=24, color='white')
    video_clip = VideoFileClip(input_path)
    subtitles_clip = SubtitlesClip(SUBTITLE_FILE_NAME, generator)
    # for (_, txt) in subtitles_clip:
    #     print(txt)
    print(subtitles_clip.duration)
    # text_clips = [TextClip(txt, fontsize=24, color='white').set_position('bottom') for (_, txt) in subtitles_clip]
    final_clip = CompositeVideoClip([video_clip, subtitles_clip])
    final_clip.duration = video_clip.duration
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # video_input_stream = ffmpeg.input(input_video)
    # stream = ffmpeg.output(video_input_stream, output_path, vf=f"subtitles={subtitle_file}")
    # ffmpeg.run(stream, overwrite_output=True, cmd=r'c:\FFmpeg\bin\ffmpeg.exe')

add_subtitles('./output/clean/tiktok.mp4', './speech.mp3', './output/final/tiktok.mp4')