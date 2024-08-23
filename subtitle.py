import math

from faster_whisper import WhisperModel

def generate_subtitles(date_str):
  # Followed this guide: https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg
  # Used this to get faster whisper working: https://stackoverflow.com/questions/66355477/could-not-load-library-cudnn-ops-infer64-8-dll-error-code-126-please-make-sure
  segments = transcribe(date_str)
  print("Transcription - complete")
  generate_file(segments, date_str)
  print("Subtitle file - created")

def transcribe(date_str):
    print("Transcribing speech...")
    audio_path = f"./output/speech/speech_{date_str}.mp3"
    model = WhisperModel("small", device="cuda", compute_type="float32", cpu_threads=4, )
    segments, _ = model.transcribe(audio_path, language='en', word_timestamps=False,  )
    segments = list(segments)
    return segments

def generate_file(segments, date_str):
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)

        # Remove first space of segment text
        segment_text = segment.text[1:] if segment.text[0] == " " else segment.text

        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment_text} \n"
        text += "\n"

    # Save subtitle file
    with open(f"./output/subtitles/sub_{date_str}.srt", "w") as f:
        f.write(text)

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time