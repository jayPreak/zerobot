import tweepy
import time
import os
import sqlite3 as db
from dotenv import load_dotenv
from keep_alive import keep_alive
import requests
import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

keep_alive()

load_dotenv()

with open('num.txt', 'r') as f:
    num = int(f.read())

apiKey = os.getenv("APIKEY")
apiKeySecret = os.getenv("APIKEY_SECRET")
bearerToken = repr(os.getenv("BEARER_TOKEN"))

accessToken = os.getenv("ACCESSTOKEN")
accessTokenSecret = os.getenv("ACCESSTOKEN_SECRET")

client = tweepy.Client(bearerToken, apiKey, apiKeySecret, accessToken,
                       accessTokenSecret)

auth = tweepy.OAuth1UserHandler(apiKey, apiKeySecret, accessToken,
                                accessTokenSecret)

api = tweepy.API(auth)

connection = db.connect("framebot.db")
cursor = connection.cursor()

show_name = "Darling In the Franxx"
github_user = "jaypreak"  # Replace with your GitHub username
repo_name = "zerobot"  # Replace with the name of your GitHub repository


def fetch_image_from_github(frame_path):
    url = f'https://raw.githubusercontent.com/{github_user}/{repo_name}/main/{frame_path}'
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open('path_to_local_image.jpg', 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return 'path_to_local_image.jpg'


while True:
    iters = 1

    while iters > 0:

        current_ep = cursor.execute(
            "SELECT current_episode FROM bot").fetchone()[0]

        ep_season, ep_num = current_ep.split('x')

        total_frames = cursor.execute("SELECT frames FROM show WHERE ep = ?",
                                      (current_ep, )).fetchone()[0]

        next_frame = cursor.execute(
            "SELECT last_frame FROM bot").fetchone()[0] + 1

        if next_frame > total_frames:
            next_ep = str(int(ep_num) + 1).zfill(2)

            if os.path.isfile(f"./frames/S{ep_season}/{next_ep}x1.jpg"):
                cursor.execute(
                    f'UPDATE bot SET current_episode = "{ep_season}x{next_ep}"')
                cursor.execute('UPDATE bot SET last_frame = ?', (0, ))
                connection.commit()
                continue

            else:
                next_season = str(int(ep_season) + 1).zfill(2)

                cursor.execute(
                    f'UPDATE bot SET current_episode = "{next_season}x01"')
                cursor.execute('UPDATE bot SET last_frame = ?', (0, ))
                connection.commit()
                continue

        frame_path = f"./frames/S{ep_season}/{ep_num}x{next_frame}.jpg"
        local_path = fetch_image_from_github(frame_path)

        msg = f"{show_name} - Season {ep_season} Episode {ep_num} - Frame {next_frame} of {total_frames}"
        media = api.media_upload(local_path)

        tweet = client.create_tweet(text=msg, media_ids=[media.media_id])
        logging.info(f'Posting frame {next_frame} of episode {current_ep}')

        # Verify that the tweet was successfully posted
        if tweet:
            cursor.execute("UPDATE bot SET last_frame = ?", (next_frame, ))
            connection.commit()

        iters -= 1

    time.sleep(3600)
