import json
from dotenv import load_dotenv
import os
import requests

from telegram import send_telegram

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

def get_post_from_url(url):
  headers = authenticate()

  # replace www.reddit.com with oauth.reddit.com
  api_url = url.replace("www.reddit.com", "oauth.reddit.com")
  # Make a GET request to the Reddit API
  res = requests.get(api_url, headers=headers)

  # Extract the title and selftext of the third post
  title = res.json()[0]['data']['children'][0]['data']['title']
  selftext = res.json()[0]['data']['children'][0]['data']['selftext']

  if len(selftext) > 4000:
    send_telegram("Post too long")
    raise ValueError("Post too long")

  return title, selftext, url

def get_post_from_sub(subreddit, listing):
  headers = authenticate()

  # Make a GET request to the Reddit API
  res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{listing}/?limit=5', headers=headers)

  def extract_post_data(response, index=1):
    if index > 4:
      send_telegram("No valid post found")
      raise ValueError("No valid post found")

    # Extract the title and selftext of the third post
    title = response.json()['data']['children'][index]['data']['title']
    selftext = response.json()['data']['children'][index]['data']['selftext']
    url = response.json()['data']['children'][index]['data']['url']

    if len(selftext) > 4000:
      title, selftext, url = extract_post_data(response, index + 1)
    
    return title, selftext, url

  # Call the function with the response object
  return extract_post_data(res)

def save_json(title, selftext):
  # Save the response as JSON
  response_json = title + "\n\n" + selftext

  # Save the JSON data to a file
  with open('./post.json', 'w') as file:
    json.dump(response_json, file)