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

api = tweepy.API(auth)
client.create_tweet(
    text="₵₳₮₵Ⱨł₦₲ ₮ⱧɆ₴Ɇ ₳ӾɆ₴ ₴Ø ł ĐØ₦₮ ₵₳₮₵Ⱨ ₣ɆɆⱠł₦₲₴ ₣ØⱤ ⱧɆⱤ ")
