# from tiktok_uploader.upload import upload_video, upload_videos
# from tiktok_uploader.auth import AuthBackend

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service

# def upload_videos(date_str='2024-08-23(1)'):
#   def setup():
#     # State the Webdriver options
#     options = webdriver.ChromeOptions()
#     # Add arguments
#     options.add_argument('--headless')
#     options.add_argument("–disable-extensions")
#     options.add_argument("–disable-gpu")
#     # Define the chrome driver path
#     ser=Service("./chromedriver/chromedriver.exe")
#     # Initiate the Chromedriver by passing options as argument
#     return webdriver.Chrome(service=ser,options=options)

#   driver = setup()
#   PATH = f"output/parts/{date_str}"
#   upload_video(f'{PATH}_part1.mp4',
#          description='this is my description',
#          cookies='cookies.txt',
#          browser_agent=driver )
 
#   driver.quit()

# upload_videos()

import requests

def get_access_token():
  url = 'https://open.tiktokapis.com/v2/oauth/token/'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cache-Control': 'no-cache'
  }
  data = {
    'client_key': 'CLIENT_KEY',
    'client_secret': 'CLIENT_SECRET',
    'code': 'CODE',
    'grant_type': 'authorization_code',
    'redirect_uri': 'REDIRECT_URI'
  }

  response = requests.post(url, headers=headers, data=data)

  # Check the response status code
  if response.status_code == 200:
    # Request was successful
    access_token = response.json().get('access_token')
    print("Access token:", access_token)
    return access_token
  else:
    # Request failed
    print("Request failed with status code:", response.status_code)
    return None

def upload_videos(date_str='2024-08-23(1)'):
  PATH = f"output/parts/{date_str}"
  
  url = 'https://open.tiktokapis.com/v2/post/publish/inbox/video/init/'
  headers = {
      'Authorization': 'Bearer act.example12345Example12345Example',
      'Content-Type': 'application/json'
  }
  data = {
      "source_info": {
          "source": "FILE_UPLOAD",
          "video_size": exampleVideoSize,
          "chunk_size" : exampleVideoSize,
          "total_chunk_count": 1
      }
  }
  
  response = requests.post(url, headers=headers, json=data)
  
  # Check the response status code
  if response.status_code == 200:
      # Request was successful
      print("Request successful!")
  else:
      # Request failed
      print("Request failed with status code:", response.status_code)

get_access_token()