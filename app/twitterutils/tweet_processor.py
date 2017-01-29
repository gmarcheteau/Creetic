#!/usr/bin/env python
import tweepy
import tweet_actions
import socket
import requests
import time
import tinyurl
from authentication import authentication
import os, sys, traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ArtyFarty import bsgenerator_en as bs_en

MY_TWEETER_NAME = "ArtyFarty7" #does not include '@'

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/
###
#tweet_data = json.loads(tweet)  # This allows the JSON data
###

### MOVE QUERY TO CONFIG
query = "#artyfartyplease OR @%s filter:media" %MY_TWEETER_NAME
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

def checkTweetsAndReply(latest_tweet_processed):

    api = prepareTweetyAPI()
    
    tweets = api.search(
      q = query,
      since_id=latest_tweet_processed,
      include_entities=True)
    
    print "Number of tweets found: %d" %len(tweets)
    
    process_responses = []
    
    for tweet in tweets:
      #update latest tweet id
      if tweet.id>latest_tweet_processed:
        latest_tweet_processed = tweet.id
      
      #don't answer to self
      if(MY_TWEETER_NAME in getUserMentionsFromTweet(tweet) and tweet.user.screen_name==MY_TWEETER_NAME):
        print "not replying to self"
        pass
      
      else:
        picurl = getPhotoUrlFromTweet(tweet)
        if picurl:
          print "IMAGE FOUND IN TWEET: %s" %picurl
          tweet_actions.replyToTweetWithSimplerImage(
            api=api,
            to_user=tweet.user.screen_name,
            status_id=tweet.id,
            picurl=picurl)
        else:
          print "NO IMAGE IN TWEET"
          tweet_actions.replyToTweet(
            api=api,
            to_user=tweet.user.screen_name,
            status_id=tweet.id)

    print "latest tweet id: %d" %latest_tweet_processed
    
    return {
      #only count tweets with images
      "number_tweets":len(process_responses),
      "process_responses":process_responses,
      "latest_tweet_id":latest_tweet_processed
      }

def getPhotoUrlFromTweet(tweet):
  
  #CHECK IF TWEET HAS MEDIA URL
  if "media" in tweet.entities and tweet.entities['media'][0]['media_url']:
    for media in tweet.entities['media']:
      #CHECK IF MEDIA IS PHOTO
      if media["type"]=="photo":
        return media['media_url']
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
