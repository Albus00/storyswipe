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
  # Followed this guide: https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg
  # Used this to get faster whisper working: https://stackoverflow.com/questions/66355477/could-not-load-library-cudnn-ops-infer64-8-dll-error-code-126-please-make-sure
  
  language, segments = transcribe(audio_path)
  subtitle_file = generate_subtitle_file(language, segments)
  render_subtitle_to_video(subtitle_file, input_path, output_path)


def transcribe(audio):
    model = WhisperModel("small", device="cuda", compute_type="float32")
    segments, info = model.transcribe(audio, beam_size=5)
    language = info[0]
    segments = list(segments)
    return language, segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(language, segments, input_video_name="video"):

    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    STYLE = """[Script Info]
Title: Default Aegisub file
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Alignment

Style: Default,Britannic Bold,24,&H000000,&H00FFFF,&H00000000,&H99000000,-1,0,6

"""

    # Save subtitle file
    subtitle_file_path = f"./{subtitle_file}"
    f = open(subtitle_file_path, "w")
    f.write(text)
    f.close()

    return subtitle_file

def render_subtitle_to_video(subtitle_file, input_video, output_video):
    # https://superuser.com/questions/874598/creating-video-containing-animated-text-using-ffmpeg-alone/874697#874697
    #     
    video_input_stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(video_input_stream, output_video, vf=f"subtitles={subtitle_file}")
    ffmpeg.run(stream, overwrite_output=True, cmd=r'c:\FFmpeg\bin\ffmpeg.exe')

add_subtitles('./output/clean/tiktok.mp4', './speech.mp3', './output/final/tiktok.mp4')