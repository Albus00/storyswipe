from moviepy.editor import VideoFileClip, AudioFileClip

def combine_sound_and_video(video_path, audio_path, output_path):
  video = VideoFileClip(video_path)
  audio = AudioFileClip(audio_path)

  video = video.set_audio(audio)
  video.write_videofile(output_path, codec='libx264', audio_codec='aac')

def add_subtitles(video_path, subtitles, output_path):
  video = VideoFileClip(video_path)
  video = video.set_audio(audio)
  video.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Example usage
video_path = './stock videos/minecraft.mp4'
audio_path = './speech.mp3'
output_path = './output/tiktok.mp4'

combine_sound_and_video(video_path, audio_path, output_path)