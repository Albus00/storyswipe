import json
from dotenv import load_dotenv
import os
import requests

def authenticate():
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

  return headers

def get_post(subreddit, listing):
  headers = authenticate()

  # Make a GET request to the Reddit API
  res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{listing}/?limit=5', headers=headers)

  def extract_post_data(response, index=1):
    if index > 4:
      raise ValueError("No valid post found")

    # Extract the title and selftext of the third post
    title = response.json()['data']['children'][index]['data']['title']
    selftext = response.json()['data']['children'][index]['data']['selftext']
    url = response.json()['data']['children'][index]['data']['url']

    if len(selftext) > 4000:
      extract_post_data(response, index + 1)
    
    return title, selftext, url

  # Call the function with the response object
  title, selftext, url = extract_post_data(res)

  return title, selftext, url

def save_json(title, selftext):
  # Save the response as JSON
  response_json = title + "\n\n" + selftext

  # Save the JSON data to a file
  with open('./post.json', 'w') as file:
    json.dump(response_json, file)