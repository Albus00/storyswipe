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

import os
from TikTokUploader.uploader import uploadVideo

def upload_videos(date_str='2024-08-23(1)'):
  PATH = f"output/parts/{date_str}"

  session_id = os.getenv("TIKTOK_SESSION_ID")
  file = f"{PATH}_part1.mp4"
  title = "MY SUPER TITLE"
  tags = ["Funny", "Joke", "fyp"]
  users = ["amazing dear"]

  # Publish the video
  uploadVideo(session_id, file, title, tags, users, url_prefix="www")

upload_videos()