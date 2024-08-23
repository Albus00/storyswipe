import os
import time
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.config import change_settings

TEMP_CLIP_PATH = "./output/temp/clip.mp4"

# Change this to the path of your ImageMagick installation (autodetection doesn't work)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def subtitle_generator(txt, fontsize=50):
    return TextClip(txt, font='Noto Sans Bold', fontsize=fontsize, color='white', method='caption', align='west', size=(500, None), stroke_color='black', stroke_width=2)

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

    ffmpeg_extract_subclip(f"./stock videos/{random_clip}", start_time, end_time, targetname=TEMP_CLIP_PATH)
    return VideoFileClip(TEMP_CLIP_PATH)

def cleanup():
    # Remove temporary files
    os.remove(TEMP_CLIP_PATH)

def render(date_str):
    # https://superuser.com/questions/874598/creating-video-containing-animated-text-using-ffmpeg-alone/874697#874697

    # Combine stock video and speech audio
    video_clip = get_footage(date_str)
    audio = AudioFileClip(f"./output/speech/speech_{date_str}.mp3")
    video_clip = video_clip.set_audio(audio)

    # Generate subtitles clip
    generator = lambda txt: subtitle_generator(txt)
    subtitles_clip = SubtitlesClip(f"./output/subtitles/sub_{date_str}.srt", generator).set_position(('center','center'))
    
    # Combine video and subtitles and render
    final_clip = CompositeVideoClip([video_clip, subtitles_clip])
    final_clip.duration = video_clip.duration
    final_clip.write_videofile(f"./output/final/final_{date_str}.mp4", codec='libx264', audio_codec='aac')

    cleanup()

def split_video(date_str):
    # Load the video clip
    video_path = f"./output/final/final_{date_str}.mp4"
    video = VideoFileClip(video_path)

    # Get the duration of the video
    duration = video.duration

    # Calculate the duration of each part
    nr_of_parts = 2
    while (part_duration := duration / nr_of_parts) > 60:
        nr_of_parts += 1
    
    print(f"Duration: {duration}, Part duration: {part_duration}")
    
    for i in range(nr_of_parts):
        part = video.subclip(i * part_duration, (i + 1) * part_duration)
        part_title_caption = subtitle_generator("Part " + str(i + 1))
        # Overlay the generator clip on the part
        part = CompositeVideoClip([part, part_title_caption.set_position(('center', 'bottom'))]) # TODO: Fix position and size
        part.duration = part_duration
        part.write_videofile(f"./output/parts/{date_str}_part{i+1}.mp4")

    # Close the video clip
    video.close()