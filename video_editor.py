import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.config import change_settings
import numpy as np
from pydub import AudioSegment, silence

TEMP_CLIP_PATH = "./output/temp/clip.mp4"

# Change this to the path of your ImageMagick installation (autodetection doesn't work)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def subtitle_generator(text, type = ""):
    if type == "part":
        return TextClip(text, font='Noto Sans Bold', fontsize=100, color='white', method='caption', align='center', size=(500, 300), stroke_color='black', stroke_width=2)
    
    return TextClip(text, font='Noto Sans Bold', fontsize=50, color='white', method='caption', align='west', size=(500, None), stroke_color='black', stroke_width=2)

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

def cleanup(temp_clip):
    # Remove temporary files
    temp_clip.close()
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

    cleanup(video_clip)

def get_silent_parts(date_str):
    print("Finding silent sections...")
    speech = AudioSegment.from_file(f"./output/speech/speech_{date_str}.mp3", format="mp3")
    silent_segments = silence.detect_nonsilent(speech, min_silence_len=1000, silence_thresh=-40)
    # Convert to array (make sure it's float64)
    silent_segments = np.array(silent_segments, dtype=np.float64)
    return silent_segments / 1000 # Convert to seconds

def find_closest_silent_part(silent_sections, time):
    for index, section in enumerate(silent_sections):
        if (time < section[0] and time > section[1]) or time < section[0]:
            return index - 1
    return len(silent_sections) - 1

def split_video(date_str):
    # Load the video clip
    video_path = f"./output/final/final_{date_str}.mp4"
    video = VideoFileClip(video_path)

    # Get the duration of the video
    duration = video.duration

    # Find where the silent parts are, to then make sure the video is split at those points
    silent_sections = get_silent_parts(date_str)
    print("Done")

    # Calculate the duration of each part
    MAX_PART_DURATION = 80
    nr_of_parts = 2
    while (part_duration := duration / nr_of_parts) > MAX_PART_DURATION:
        nr_of_parts += 1
    
    prev_ending = 0
    for i in range(nr_of_parts):
        # Find the silent part that is closest to the end of this part
        part_ending_time = prev_ending + part_duration
        print(f"Part {i+1} ending time: {part_ending_time}")
        # Find the index of the silent part that is closest to the ending time
        index = find_closest_silent_part(silent_sections, part_ending_time)
        part_ending_time = silent_sections[index][0]
        print(f"Silent part found at: {part_ending_time}")

        # Split the video at the silent part
        print(f"Splitting video at {prev_ending} and {part_ending_time}")
        part = video.subclip(prev_ending, part_ending_time)
        
        # Add a "Part x" caption to the video
        part_title_caption = subtitle_generator(type="part", text="Part " + str(i + 1))
        part = CompositeVideoClip([part, part_title_caption.set_position(('center', 'bottom'))]) # TODO: Fix position and size
        part.duration = part_ending_time - prev_ending
        part.write_videofile(f"./output/parts/{date_str}_part{i+1}.mp4")
        prev_ending = part_ending_time

    # Close the video clip
    video.close()

split_video("2024-08-23(1)")