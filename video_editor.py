import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.config import change_settings
import os

# Change this to the path of your ImageMagick installation (autodetection doesn't work)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def get_footage(date_str):
    def nr_of_clips(folder_path):
        file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        return file_count
    
    def get_speech_length():
        audio = AudioFileClip(f"./output/speech/speech_{date_str}.mp3")
        speech_length = audio.duration
        return speech_length
    
    def get_random_clip():
        num_clips = nr_of_clips('./stock videos')
        if num_clips > 1:
            random_clip = f"minecraft{random.randint(1, num_clips)}.mp4"
        elif num_clips == 1:
            random_clip = "minecraft1.mp4"
        else:
            raise ValueError("No stock footage found")
            
        return random_clip
    
    def get_random_time(stock_length, clip_length):
        print(f"Stock length: {stock_length}, clip length: {clip_length}")
        start_time = random.randint(0, int(stock_length - clip_length))
        end_time = start_time + clip_length
        return start_time, end_time

    random_clip = get_random_clip()
    print(f"Using stock footage: {random_clip}")
    random_clip_length = VideoFileClip(f"./stock videos/{random_clip}").duration
    start_time, end_time = get_random_time(random_clip_length, get_speech_length())

    # TODO: Resize video to phone aspect ratio
    # .resize(width=1080/(16/9))

    ffmpeg_extract_subclip(f"./stock videos/{random_clip}", start_time, end_time, targetname="./output/temp/clip.mp4")
    return VideoFileClip("./output/temp/clip.mp4")

def render(date_str):
    # https://superuser.com/questions/874598/creating-video-containing-animated-text-using-ffmpeg-alone/874697#874697

    # Combine stock video and speech audio
    video_clip = get_footage(date_str)
    audio = AudioFileClip(f"./output/speech/speech_{date_str}.mp3")
    video_clip = video_clip.set_audio(audio)

    # Generate subtitles clip
    generator = lambda txt: TextClip(txt, font='Noto Sans Bold', fontsize=50, color='white', method='caption', align='West', size=(500, None), stroke_color='black')
    subtitles_clip = SubtitlesClip(f"./output/subtitles/sub_{date_str}.srt", generator).set_position(('center','center'))
    
    # Combine video and subtitles and render
    final_clip = CompositeVideoClip([video_clip, subtitles_clip])
    final_clip.duration = video_clip.duration
    final_clip.write_videofile(f"./output/final/final_{date_str}.mp4", codec='libx264', audio_codec='aac')

# combine_sound_and_video('./stock videos/minecraft1.mp4', './speech.mp3', './output/final/tiktok.mp4')
# add_subtitles('./stock videos/minecraft1.mp4', './speech.mp3', './output/final/tiktok.mp4')