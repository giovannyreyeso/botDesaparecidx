import tweepy
import time
from bot_wit import BotWit

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
WIT_AI_SECRET = ''

id_mexico = 110978
bot_id = '143555567'
file_name = 'last_seen_id.txt'
keywords = [
    "#desaparecido", "#desaparecida", 
    "#alertaamber", "#teestamosbuscando", 
    "#alertadebusqueda"
]
result_types = ['recent', 'popular']
searchword = []
date_since = '2019-11-01'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
bot_wit = BotWit(WIT_AI_SECRET)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

#mention function
def search_function():
    try:
        last_seen_id = retrieve_last_seen_id(file_name)
        print(last_seen_id)
        mentions = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')
        #goes through all mentions
        for mention in (mentions):
            print("Found mention!")
            print(str(mention.id) + ' - ' + mention.full_text)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, file_name)
            #follows user who mentions
            if not mention.user.following and mention.user.id != bot_id:
                mention.user.follow()
            #if mention is not a retweet
            if not mention.retweeted:
                #if is a reply
                if mention.in_reply_to_status_id is not None:
                    replyid = mention.in_reply_to_status_id
                    newuser = api.get_status(replyid)
                    #check if it is following itself
                    if newuser.user.id != bot_id:
                        #follows original tweet
                        if not newuser.user.following:
                            newuser.user.follow()
                        #retweets original retweets
                        if not newuser.retweeted:
                            newuser.retweet()
                else:
                    mention.retweet()             
        except tweepy.TweepError as e:
            print(e)
            print("follow error")

#searching search_function
def main():
    try:
        foundtweets = False
        #words loop
        for i in range(len(keywords)):
            tweetcont = 0
            searchword.append(keywords[i] + " -filter:retweets")
            print("Looking for tweets with " + keywords[i])
            #search for recent and popular
            for j in range(len(result_types)):
                tweets = tweepy.Cursor(api.search,q=searchword[i],count=100,
                    geocode='23.634,-102.55,500km',lang='es',
                    result_type=result_types[j],
                    since=date_since).items(100)
                #search each tweet
                for tweet in tweets:
                    #3 tweets per keyword
                    if tweetcont != 3:
                        if not tweet.retweeted:
                            print(tweet.text)
                            print(tweet.user.location)
                            print(tweet.id)
                            tweet.retweet()
                            tweetcont = tweetcont + 1
                            api.update_status('@' + tweet.user.screen_name + ' Hola! Soy un bot que te \
                                ayudará a difundir tu caso, sígueme!', tweet.id)
                            print("New tweet found!")
                            print("Checking mentions...")
                            search_function()
                            foundtweets = True
                            time.sleep(1200)
                        else:
                            print("Repeats!")
                    else:
                        print("max tweets")
                        break                                        
        #no tweets found, check mentions
        if not foundtweets:
        print("Checking mentions...")
        search_function()
        time.sleep(1200)            
    except tweepy.TweepError as e:
    print(e)
    print("Repeats!")
#loop
while True:
    print("Checking tweets...")
    main()
    time.sleep(5)
