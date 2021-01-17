from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import packages

#fill these in
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
                #checks if the tweet was a retweeted tweet (by a different user), if yes, the correct user id and tweet.text will be placed for the database
                if tweet.entities['user_mentions'][0]['id'] == tweet.retweeted_status.user.id:
                    tweet.user.id = tweet.entities['user_mentions'][0]['id']
                    tweet.text = tweet.text.split(' ', 2)[2] 
                #this is to make sure that replies that were retweets will not appears as non replies, remove if "if tweet.in_reply_to_status_id == None:" is not necesary
                if tweet.retweeted_status.id != None:
                    tweet.in_reply_to_status_id = tweet.retweeted_status.id
            except:
                pass
            #checks if the user is in the blocked database
            if packages.checkblock(tweet, self.api) == False:
                #checks if the tweet was retweeted by the bot already
                if self.api.get_status(tweet.id).retweeted == False:
                    #checks if the tweet is a quote retweet, remove if not requrired
                    if tweet.is_quote_status == False:
                        #checks if the tweet is a reply, remove if not requrired
                        if tweet.in_reply_to_status_id == None:
                            #checks if the tweet contains and muted words
                            if packages.mute(tweet) == True:
                                try:
                                    #retweets the tweet
                                    packages.retweet(tweet, self.api)
                                except BaseException as e:
                                        print("Error at retweet (main.py) %s" % str(e))
                        #if the tweet was a reply, if sends in the mainuse function
                        if tweet.in_reply_to_status_id != None:
                            packages.mainuse(tweet, self)
            
        except BaseException as e:
            print("Error on_status %s" % str(e))
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    
    #replace this with the word/s that needs to be retweeted
    hash_tag_list = [""]

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)
