from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import re

##update the 5 variables below, hashtag list, censor words and retweet words

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
userat = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)


class TwitterStreamer():

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
            if tweet.is_quote_status == False:
                if tweet.retweeted == False:
                    if tweet.in_reply_to_status_id == None:
                        ##censor words
                        if re.findall("", tweet.text):
                            return
                        ##retweet words
                        if re.findall("", tweet.text):
                            tweet.retweet()
                            print("retweeted")
                            return

                    if (tweet.in_reply_to_status_id != None):
                        if re.findall("bot rt this", tweet.text):
                            if (tweet.user.screen_name == userat):
                                tweet.id = tweet.in_reply_to_status_id
                                tweet.retweet()
                                print("retweeted the tweet above")

                        if re.findall("bot urt this", tweet.text):
                            if (tweet.user.screen_name == userat):
                                tweet.id = tweet.in_reply_to_status_id
                                self.api.unretweet(tweet.id)
                                print("unretweeted the tweet above")

                        if re.findall("bot like this", tweet.text):
                            if (tweet.user.screen_name == userat):
                                tweet.id = tweet.in_reply_to_status_id
                                tweet.favorite()
                                print("liked the tweet above")

                        if re.findall("bot unlike this", tweet.text):
                            if (tweet.user.screen_name == userat):
                                tweet.id = tweet.in_reply_to_status_id
                                self.api.destroy_favorite(tweet.id)
                                print("unliked the tweet above")

        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    hash_tag_list = [""]

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)
