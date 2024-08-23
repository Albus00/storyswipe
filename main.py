import datetime
import random
from import_posts import get_post
from filter_words import filter_swear_words, filer_shortening
from generate_voice import text_to_speech
from subtitle import generate_subtitles
from video_editor import render

FIXED_ID = 1

SUBREDDIT = "AmITheAsshole"
LISTING = "hot"
VOICE = "echo"
CLEAN_POST = False

post = get_post(SUBREDDIT, LISTING)
print(f"Starting to generate video for post: {post[0]}")

# TODO: Add screenshots using playwright

if CLEAN_POST:
    post = filter_swear_words(post[0]), filter_swear_words(post[1])
    print("Post cleaned from swear words")

manuscript = filer_shortening(post[0]), filer_shortening(post[1])

# Get today's date and random id for file naming
today = datetime.date.today()
if FIXED_ID == 0:
    date_str = today.strftime("%Y-%m-%d") + "(" + str(random.randint(0, 1000)) + ")"
else:
    date_str = today.strftime("%Y-%m-%d") + "(" + str(FIXED_ID) + ")"

print(f"Generated date string: {date_str}")

text_to_speech(date_str, manuscript, VOICE)

generate_subtitles(date_str)

render(date_str)