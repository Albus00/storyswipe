from import_posts import get_post
from filter_words import filter_swear_words, filer_shortening
from generate_voice import text_to_speech

SUBREDDIT = "AmITheAsshole"
LISTING = "hot"
VOICE = "echo"

post = get_post(SUBREDDIT, LISTING)

print(post[2])

# cleaned_post = filter_swear_words(post[0]), filter_swear_words(post[1])

manuscript = filer_shortening(post[0]), filer_shortening(post[1])
print(manuscript)

text_to_speech("./", manuscript, VOICE)