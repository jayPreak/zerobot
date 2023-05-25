import tweepy
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

api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")

except:
    print("Error during authentication")

api.update_status(
    "L9 FAKER HAS MY IP ADRESS PLEASE DONT @ HIM IN GENERAL ON RATIRL SERVER I BEG U")
