import json
from dotenv import load_dotenv
import os
import requests

# Load environment variables from the .env file
load_dotenv()

# Make authentication request
app_id = os.getenv("REDDIT_APP_ID")
secret = os.getenv("REDDIT_APP_SECRET")
auth = requests.auth.HTTPBasicAuth(app_id, secret)
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")

data = {
    'grant_type': 'password',
    'username': reddit_username,
    'password': reddit_password
}
headers = {'User-Agent': 'Tutorial2/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# Extract the access token from the response
access_token = res.json()['access_token']

# Update headers with the access token
headers.update({"Authorization": f"bearer {access_token}"})

# Make a GET request to the 'all' subreddit's top posts endpoint
res = requests.get('https://oauth.reddit.com/r/AskReddit/top/?limit=1', headers=headers)

# Extract the titles of the top 10 posts
# titles = [post['data']['title'] for post in res.json()['data']['children']]

# # Print the titles
# for title in titles:
#     print(title)

# Save the response as JSON
response_json = res.json()

# Save the JSON data to a file
with open('./top.json', 'w') as file:
  json.dump(response_json, file)
