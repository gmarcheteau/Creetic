#!/usr/bin/env python
import tweepy
import socket
import requests
import time
import tinyurl
from authentication import authentication
import os, sys, traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ArtyFarty import bsgenerator_en as bs_en
from ArtyFarty import imageapp

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/

###
#tweet_data = json.loads(tweet)  # This allows the JSON data
###

'''
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
'''

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

'''
tweets = api.home_timeline()
for tweet in tweets:
  print tweet.id
  try:
    api.destroy_status(tweet.id)
  except:
    print "error"
'''