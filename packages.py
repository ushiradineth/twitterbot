import re
import tweepy
from tinydb import TinyDB, Query
from tinydb.operations import increment
import sys

s = 0

"""
this function is used to see if the user is following a certain account (or multiple)
it checks the database to see if the user is a pre-existing user, if not the bot will check if the user follows a certain
make sure to fill in the target_screen_name (line 26 and 43) in both isfollowing and isfollowingapi
pre-existing user means the user was already checked
if this function is not necessary, remove or comment out the isfollowing and isfollowingapi functions and the function call in the retweet function
"""

def isfollowing(tweet, api):
    try:
        db = TinyDB('db.json')
        t = Query()
        db.search(t.user == tweet.user.id)[0]
        return True
 
    except:
        try:
            if ((api.show_friendship(source_id=tweet.user.id,target_screen_name=""))[0].following) == True:
                return True
        except:
            return isfollowingapi(tweet)
            
"""
This function is used by the previous function in case it was unable to check the user's following, which usually occurs due to rate limits
so this function will switch auth to a different app and try again, multiple app tokens keys should be set in the last bit of the application for this function to work
make sure to fill in the target_screen_name (line 26 and 43) in both isfollowing and isfollowingapi
"""

def isfollowingapi(tweet):
    global s
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY_LIST_VERIFY[s], CONSUMER_SECRET_LIST_VERIFY[s])
        auth.set_access_token(ACCESS_TOKEN_LIST_VERIFY[s], ACCESS_TOKEN_SECRET_LIST_VERIFY[s])
        api = tweepy.API(auth)            
        
        if ((api.show_friendship(source_id=tweet.user.id,target_screen_name=""))[0].following) == True:
            return True

    except BaseException as e:
        print("Error at isfollowingapi (packages.py) %s" % str(e))
        if s == sys.getsizeof(ACCESS_TOKEN_LIST_VERIFY):
            s = 0
        else:
            s += 1
        return isfollowingapi(tweet)
       
       
"""
This function checks the isfollowing function to make sure the user is following a certain other user (unless removed) and retweets the tweet if the word is found the in tweet.text
if the tweet should also be liked, "tweet.favorite()" right under tweet.retweet()
make sure to fill in the quotes with the word that needs to be retweeted in both line 65 and 68
"""

def retweet(tweet, api):
    try:
        if isfollowing(tweet, api) == True:
            if re.findall("", tweet.text):
                tweet.retweet()
                tweet.favorite()
                db(tweet, api, "")
                return

    except BaseException as e:
            print("Error retweet (packages.py) %s" % str(e))

"""
This function will ignore any tweets that has the following word
fill in the word at line 80
remove if unnecessary (make sure to remove the function call in main.py)
"""

def mute(tweet):
    if re.findall("", tweet.text):
        return False
    return True
    
"""
This function allows the user to control the bot over a different account
fill in the word at line 80
remove if unnecessary (make sure to remove the function call in main.py)
in every command make sure to put the "replacethis with the keyword that the retweet bot looks for
in every command make sure to change the tweet.user.screen_name to the account that controls the main account
to control this over twitter, tweet a dot or anything and then reply any command (the command tweet will be liked by the bot account to show that it worked)
for the last command "replacethis bot block " : in the command tweet, the user that needs to be blocked should be specified, eg: "replacethis bot block twitter"
"""

def mainuse(tweet, self):
    try:
        if re.findall("replacethis bot rt this", tweet.text):
            if tweet.user.screen_name == "":
                tweet.favorite()
                tweet.id = tweet.in_reply_to_status_id
                tweet.retweet()
            return

        if re.findall("replacethis bot urt this", tweet.text):
            if tweet.user.screen_name == "":
                tweet.favorite()
                tweet.id = tweet.in_reply_to_status_id
                self.api.unretweet(tweet.id)
            return

        if re.findall("replacethis bot like this", tweet.text):
            if tweet.user.screen_name == "":
                tweet.favorite()
                tweet.id = tweet.in_reply_to_status_id
                tweet.favorite()
            return

        if re.findall("replacethis bot unlike this", tweet.text):
            if tweet.user.screen_name == "":
                tweet.favorite()
                tweet.id = tweet.in_reply_to_status_id
                self.api.destroy_favorite(tweet.id)
            return

        if re.findall("replacethis bot block ", tweet.text):
            if tweet.user.screen_name == "":
                t = tweet.text
                first, *middle, last = t.split()
                dbblock(last, self.api)
                tweet.favorite()
            return
        
    except BaseException as e:
            print("Error mainuse (packages.py) %s" % str(e))
 
"""
database for the ammount of times users got retweeted with specific word
checks if the user pre-exists, if yes will update the word and total, if not, will insert a field for the user and add the word and total and set is both to 1 along with the twitter id
"""
def db(tweet, api, word):
    db = TinyDB('db.json')
    t = Query()

    try: 
        db.search(t.user == tweet.user.id)[0]
        db.update(increment('total'), t.user == tweet.user.id)
        try:
            db.search(t[word].exists())
            db.update(increment(word), t.user == tweet.user.id)
        except:
            db.update({word : 1}, t.user == tweet.user.id)
    except:
        db.insert({'user': tweet.user.id, 'total': 1, word : 1})

    db.close()

"""
database for blocked user (from mainuse function)
blocked does not mean a twitter block, rather the bot will ignore tweets from these users
will add the twitter id and will delete the users data from the main database
"""
def checkblock(tweet, api):
    db = TinyDB('blocklist.json')
    t = Query()

    try:
        db.search(t.user == tweet.user.id)[0]
        return True
    except:
        return False

def dbblock(username, api):
    db = TinyDB('blocklist.json')
    dbdbase = TinyDB('db.json')
    t = Query()

    id = api.get_user(screen_name = username).id

    db.insert({'user': id})
    dbdbase.remove(t.user == id)

    db.close()
    dbdbase.close()
    
#replace these keys for function isfollowingpapi , is recomemded to have multiple apps

ACCESS_TOKEN_LIST_VERIFY = [
    ""
]
ACCESS_TOKEN_SECRET_LIST_VERIFY = [
    ""
]
CONSUMER_KEY_LIST_VERIFY = [
    ""
]
CONSUMER_SECRET_LIST_VERIFY = [
    ""
]
