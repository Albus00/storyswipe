import os
import sys 
import datetime
import random
from import_posts import get_post_from_sub, get_post_from_url
from filter_words import filter_swear_words, filer_shortening
from generate_voice import text_to_speech
from subtitle import generate_subtitles
from telegram import send_telegram
from video_editor import render

FIXED_ID = 1
SKIP_TTS = True

SUBREDDIT = "AmITheAsshole"
LISTING = "hot"
VOICE = "echo"
CLEAN_POST = True

def setup():
    # Create the output folders if they don't exist
    os.makedirs("./output/parts", exist_ok=True)
    os.makedirs("./output/speech", exist_ok=True)
    os.makedirs("./output/temp", exist_ok=True)
    os.makedirs("./output/subtitles", exist_ok=True)
    print("Setup complete")


# Setup the output folders
setup()

if len(sys.argv) > 1:
    # Get the post from the command line arguments
    post = get_post_from_url(sys.argv[1])
    print(f"\nStarting to generate video for post: {post[0]}\n")
else:
    # Get the post from the subreddit
    post = get_post_from_sub(SUBREDDIT, LISTING)
    print(f"\nStarting to generate video for post: {post[0]}\n")

send_telegram("Starting to generate video for post: " + post[0] +"\n" + post[2])
# TODO: Add screenshots using playwright

if CLEAN_POST:
    # Clean the post from swear words
    post = filter_swear_words(post[0]), filter_swear_words(post[1]), post[2]
    print("Post cleaned from swear words")

manuscript = filer_shortening(post[0]), filer_shortening(post[1])

# Get today's date and random id for file naming
today = datetime.date.today()
if FIXED_ID == 0:
    date_str = today.strftime("%Y-%m-%d") + "(" + str(random.randint(0, 1000)) + ")"
else:
    date_str = today.strftime("%Y-%m-%d") + "(" + str(FIXED_ID) + ")"

print(f"Generated date string: {date_str}")

if not SKIP_TTS:
    text_to_speech(date_str, manuscript, VOICE)

# generate_subtitles(date_str)

# render(date_str)