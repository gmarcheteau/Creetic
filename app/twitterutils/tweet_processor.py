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

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/
###
#tweet_data = json.loads(tweet)  # This allows the JSON data
###
  
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
      q = "#ArtyFartyPlease",
      since_id=latest_tweet_processed,
      include_entities=True)
    
    print "Number of tweets found: %d" %len(tweets)
    
    process_responses = []
    
    for tweet in tweets:
      #update latest tweet id
      if tweet.id>latest_tweet_processed:
        latest_tweet_processed = tweet.id
      
      picurl = getPhotoUrlFromTweet(tweet)
      tweet_actions.replyToTweet(
        api=api,
        to_user=tweet.user.screen_name,
        status_id=tweet.id,
        picurl=picurl) #if picurl is Null, will generate a simple comment
    
  
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