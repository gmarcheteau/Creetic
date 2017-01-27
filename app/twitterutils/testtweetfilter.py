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

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/

###
#tweet_data = json.loads(tweet)  # This allows the JSON data
###





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

query = ["ArtyFarty7"]

tweets = api.search(q = query)

print "Number of tweets found: %d" %len(tweets)

for tweet in tweets:
  print "From: @%s" %tweet.user.screen_name
  print "Date: %s" %str(tweet.created_at)
  print "Text: %s" %tweet.text
  if tweet.entities['user_mentions']:
    print "User mentions:"
    for mention in tweet.entities["user_mentions"]:
      print "@%s" %mention["screen_name"]
  if tweet.entities['hashtags']:
    print "Hashtags:"
    for hashtag in tweet.entities["hashtags"]:
      print "#%s" %hashtag["text"]
  print '-----'
  print tweet._json

