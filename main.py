from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import packages

ACCESS_TOKEN = packages.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = packages.ACCESS_TOKEN_SECRET
CONSUMER_KEY = packages.CONSUMER_KEY
CONSUMER_SECRET = packages.CONSUMER_SECRET


class TwitterStreamer:
    def __init__(self):
        pass

    def stream_tweets(self, hash_tag_list):

        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        listener = FavRetweetListener(api=tweepy.API(auth))
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):

        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
     
        try:
            try:
                if self.api.get_status(tweet.id).entities['user_mentions'][0]['id'] == self.api.get_status(tweet.id).retweeted_status.user.id:
                    tweet.user.id = self.api.get_status(tweet.id).entities['user_mentions'][0]['id']
            except:
                pass
            if self.api.get_status(tweet.id).retweeted == False:
                packages.retweet(tweet, self.api)
        except BaseException as e:
            print("Error on main.py @on_status %s" % str(e))
            return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":

    hash_tag_list = ["word"]

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)
