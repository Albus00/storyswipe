from import_posts import get_post
# from generate_voice import generate_voice

SUBREDDIT = "AmITheAsshole"
LISTING = "hot"

post = get_post(SUBREDDIT, LISTING)

print(post)