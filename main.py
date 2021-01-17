from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import packages

ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 
CONSUMER_KEY = 
CONSUMER_SECRET = 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

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
            tweet.text = tweet.text.lower()
            try:
                if tweet.entities['user_mentions'][0]['id'] == tweet.retweeted_status.user.id:
                    tweet.user.id = tweet.entities['user_mentions'][0]['id']
                    tweet.text = tweet.text.split(' ', 2)[2] 
                if tweet.retweeted_status.id != None:
                    tweet.in_reply_to_status_id = tweet.retweeted_status.id
            except:
                pass
            if packages.checkblock(tweet, self.api) == False:
                if self.api.get_status(tweet.id).retweeted == False:
                    if tweet.is_quote_status == False:
                        if tweet.in_reply_to_status_id == None:
                            if packages.mute(tweet) == True:
                                try:
                                    packages.retweet(tweet, self.api)
                                except BaseException as e:
                                        print("Error at retweet (main.py) %s" % str(e))

                        if tweet.in_reply_to_status_id != None:
                            packages.mainuse(tweet, self)
            
        except BaseException as e:
            print("Error on_status %s" % str(e))
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":

    hash_tag_list = [""]

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)
