from openai import OpenAI

def text_to_speech(date_str, manuscript, voice):
  client = OpenAI()

  # Make sure the voice is valid
  if voice not in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
    raise ValueError("Invalid voice")

  # Combine the title and selftext
  manuscript = manuscript[0] + " " + manuscript[1]

  speech_file_path = f"./output/speech/speech_{date_str}.mp3"

  print("Generating speech...")
  response = client.audio.speech.create(
    model="tts-1",
    voice=voice,
    input=manuscript
  )
  response.stream_to_file(speech_file_path)
  print("Speech - generated")
  