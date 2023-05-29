import tweepy
import sqlite3 as db
import os
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("APIKEY")
apiKeySecret = os.getenv("APIKEY_SECRET")
bearerToken = repr(os.getenv("BEARER_TOKEN"))

accessToken = os.getenv("ACCESSTOKEN")
accessTokenSecret = os.getenv("ACCESSTOKEN_SECRET")

client = tweepy.Client(bearerToken, apiKey, apiKeySecret,
                       accessToken, accessTokenSecret)

auth = tweepy.OAuth1UserHandler(
    apiKey, apiKeySecret, accessToken, accessTokenSecret)

api = tweepy.API(auth)


connection = db.connect("framebot.db")
cursor = connection.cursor()


show_name = "Darling In the Franxx"


iters = 1

while iters > 0:

    current_ep = cursor.execute(
        "SELECT current_episode FROM bot").fetchone()[0]

    ep_season, ep_num = current_ep.split('x')

    total_frames = cursor.execute(
        f"SELECT frames FROM show WHERE ep = \"{current_ep}\"").fetchone()[0]

    next_frame = cursor.execute("SELECT last_frame FROM bot").fetchone()[0] + 1

    if next_frame > total_frames:
        next_ep = str(int(ep_num)+1).zfill(2)

        if os.path.isfile(f"./frames/S{ep_season}/{next_ep}x1.jpg"):
            cursor.execute(
                f'UPDATE bot SET current_episode = "{ep_season}x{next_ep}"')
            cursor.execute(f'UPDATE bot SET last_frame = 0')
            connection.commit()
            continue

        else:
            next_season = str(int(ep_season) + 1).zfill(2)

            cursor.execute(
                f'UPDATE bot SET current_episode = "{next_season}x01"')
            cursor.execute(f'UPDATE bot SET last_frame = 0')
            connection.commit()
            continue

    frame_path = f"./frames/S{ep_season}/{ep_num}x{next_frame}.jpg"

    msg = f"{show_name} - Season {ep_season} Episode {ep_num} - Frame {next_frame} of {total_frames}"
    media = api.media_upload(frame_path)

    client.create_tweet(text=msg, media_ids=[media.media_id])

    cursor.execute(f"UPDATE bot SET last_frame = {next_frame}")
    connection.commit()

    iters -= 1
