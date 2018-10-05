#!/usr/bin/env python
import tweepy
import tweet_actions
import socket
import requests
import time
import json
import tinyurl
import random
from authentication import authentication
import os, sys, traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ArtyFarty import bsgenerator_en as bs_en
from config import TWITTER_ON,MAX_NUMBER_OF_TWEETOUTS_PER_SESSION

#MY_TWEETER_NAME = "CreeticBot" #does not include '@'
HASHTAGS = [
  "modernart",
  "abstractart",
  "abstractpainting",
  "artyfarty",
  "artyfartyplease",
  "creeticbot",
  "creetic"
  ]#does not include '#'

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/
###
#tweet_data = json.loads(tweet)  # This allows the JSON data
###

### TODO: MOVE QUERY TO CONFIG?
###BUILD QUERY ###
query = ''
for hashtag in HASHTAGS:
  query+="#%s OR " %hashtag
query=query[:-3] ##remove the last "OR"
query += "filter:media"
print "Twitter query: %s" %query
### END OF MOVE QUERY TO CONFIG

def prepareTweetyAPI():
  # Get access and key from another class
  auth = authentication()

  consumer_key = auth.getconsumer_key()
  consumer_secret = auth.getconsumer_secret()

  access_token = auth.getaccess_token()
  access_token_secret = auth.getaccess_token_secret()

  # Authentication
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.secure = True
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)
  return api

def foundTweetsToReplyTo(latest_tweet_processed):
  status = ""
  
  api = prepareTweetyAPI()
  
  tweets = api.search(
    q = query,
    since_id=latest_tweet_processed,
    include_entities=True)
  
  if tweets:
    
    print "\n###READING TWEETS###"
    print "Number of tweets found: %d \n" %len(tweets)
    
    #update latest tweet id
    for tweet in tweets:
      print "ID: %s" %str(tweet.id)
      print "Date: %s" %str(tweet.created_at)
      if tweet.id>latest_tweet_processed:
        latest_tweet_processed = tweet.id
    print "###END OF READING TWEETS###\n"
    
    ###SELECT UP TO MAX_NUMBER_OF_TWEETOUTS_PER_SESSION to reply to
    randomNumbers = random.sample(range(len(tweets)-1),min(len(tweets),MAX_NUMBER_OF_TWEETOUTS_PER_SESSION))
    print "random Tweet # selected: %s" %randomNumbers
    
    for tweetPosition in randomNumbers:
        #select 1 random tweet to reply to
        #tweet = selectRandomTweet(tweets)
        tweet = tweets[tweetPosition]
        
        if tweet:
            picurl = getPhotoUrlFromTweet(tweet)
            print "Date: %s" %tweet.created_at
            print "IMAGE FOUND IN TWEET: %s" %picurl
      
            if picurl:
                print "picurl OK"
                ##REPLY WITH IMAGE
                status+= tweet_actions.replyToTweetWithSimplerImage(
                api=api,
                to_user=tweet.user.screen_name,
                status_id=tweet.id,
                picurl=picurl)
                status+='\n'
        
            else:
                print "picurl NOT OK \n"

                ##REPLY WITHOUT IMAGE
                status = tweet_actions.replyToTweet(
                api=api,
                to_user=tweet.user.screen_name,
                status_id=tweet.id)
        else:
            status+= "no tweet with photo found \n"
    else:
        status+= "not tweets found \n"

        print status
  
  return {
    "number_tweets_found":len(tweets),
    "status":status,
    "latest_tweet_id":latest_tweet_processed
    }
 
def getPhotoUrlFromTweet(tweet):
  print "***Printing tweet data from getPhotoUrlFromTweet*** \n"
  print json.dumps(
    tweet.entities,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
    )
  #CHECK IF TWEET HAS MEDIA URL
  if "media" in tweet.entities and tweet.entities['media'][0]['media_url']:
    for media in tweet.entities['media']:
      #CHECK IF MEDIA IS PHOTO
      if media["type"]=="photo":
        #return media['media_url']
        print "def getPhotoUrlFromTweet(tweet) -- URL found: %s" % media.get('media_url')
        return media.get('media_url')
      else:
        pass
  
  else:
    return None

def getUserMentionsFromTweet(tweet):
  user_mentions = []
  #CHECK IF TWEET HAS USER MENTIONS
  if "user_mentions" in tweet.entities:
    for mention in tweet.entities["user_mentions"]:
      user_mentions.append(mention["screen_name"])
    return user_mentions
  else:
    return None

def getHashtagsFromTweet(tweet):
  hashtags = []
  if tweet.entities['hashtags']:
    for hashtag in tweet.entities["hashtags"]:
      hashtags.append(hashtag["text"])
    return hashtags
  else:
    return None


def selectRandomTweet(tweets):
  rand = random.randint(0,len(tweets)-1)
  tweet = tweets[rand]
  counter = 0
   
  """ THIS BLOCK WOULD LOOP THROUGH TWEETS UNTIL FINDING A PIC WITH URL. TOO MANY FLASE NEGATIVES
  #choose new tweet until one has photo
  while not getPhotoUrlFromTweet(tweet) and counter<len(tweets):
    print "attempt #%d - tweet didn't have photo, selecting different one" %(counter+1)
    tweet=tweets[(rand+1)%len(tweets)]
    counter+=1
  
  if not getPhotoUrlFromTweet(tweet):
    print "unable to retrieve tweet with photo"
    return None
  else:
    print "returning tweet %s" %tweet.id
    return tweet
  """
  return tweet 
  
def manualTweetReply(tweetid):
  print "Manual tweetOut"
  api = prepareTweetyAPI()
  tweet = api.get_status(tweetid)
  
  picurl = getPhotoUrlFromTweet(tweet)
  print "Date: %s" %tweet.created_at
  print "IMAGE FOUND IN TWEET: %s" %picurl
  
  ##REPLY
  status = tweet_actions.replyToTweetWithSimplerImage(
    api=api,
    to_user=tweet.user.screen_name,
    status_id=tweet.id,
    picurl=picurl)
  
  return {
  "status":status,
  "mode":"manual tweetOut"
  }
