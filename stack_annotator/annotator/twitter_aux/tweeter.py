import os
import requests
from requests_oauthlib import OAuth1

POST_STATUS_TWITTER_URL = "https://api.twitter.com/1.1/statuses/update.json"

# our app key and secret we get from the twitter app site
CONSUMER_KEY = os.environ['SA_CONSUMER_KEY'] 
CONSUMER_SECRET = os.environ['SA_CONSUMER_SECRET'] 

# get the below through calling API
ACCESS_TOKEN = os.environ['SA_ACCESS_TOKEN'] 
ACCESS_TOKEN_SECRET = os.environ['SA_ACCESS_TOKEN_SECRET']

# tweet this out!
def send_tweet(message):
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    r = requests.post(POST_STATUS_TWITTER_URL, data = {'status' : message}, auth=auth)


# tweeter = stackAnnotator_tweeter();
# tweeter.send_tweet("My first twitter posts Backend")