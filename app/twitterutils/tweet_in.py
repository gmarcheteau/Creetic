#!/usr/bin/env python
import tweepy
import tweet_actions
import socket
import requests
import time
import json
import tinyurl
from authentication import authentication
import os, sys, traceback
from config import MY_TWITTER_ID,MY_TWITTER_NAME

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ArtyFarty import bsgenerator_en as bs_en

#MY_TWITTER_NAME does not include '@'
HASHTAG = "creetic" #does not include '#'

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/
###
#tweet_data = json.loads(tweet)  # This allows the JSON data
###

### MOVE QUERY TO CONFIG
#query = "#%s OR @%s filter:media" %(HASHTAG,MY_TWITTER_NAME) #get tweets with hashtag or mentions
query = "#%s OR @%s" %(HASHTAG,MY_TWITTER_NAME) #get tweets with hashtag or mentions EVEN WITHOUT MEDIA
#query = "#%s filter:media" %HASHTAG
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
    
    print "Twitter Query: %s" %query
    print "Number of tweets found: %d" %len(tweets)
    
    numberTweets = len(tweets)
    tweetsSent = 0
    tweetsNotSent = 0
    
    for tweet in tweets:
      print tweet
      
      #update latest tweet id
      if tweet.id>latest_tweet_processed:
        latest_tweet_processed = tweet.id
      
      #don't answer to self
      if(MY_TWITTER_NAME in getUserMentionsFromTweet(tweet) and tweet.user.screen_name==MY_TWITTER_NAME):
        tweetsNotSent+=1
        print "not replying to self"
        pass
      
      #don't reply to replies
      if tweet_actions.isReplyingToMe(tweet):
        tweetsNotSent+=1
        print "not replying to replies"
        pass
      
      else:
        print "isReplyingToMe: %s" %tweet_actions.isReplyingToMe(tweet)
        picurl = getPhotoUrlFromTweet(tweet)
        if picurl:
          print "IMAGE FOUND IN TWEET: %s" %picurl
          tweetsSent+=1
          tweet_actions.replyToTweetWithSimplerImage(
            api=api,
            to_user=tweet.user.screen_name,
            status_id=tweet.id,
            picurl=picurl)
        else:
          print "NO IMAGE IN TWEET"
          tweetsSent+=1
          tweet_actions.replyToTweet(
            api=api,
            to_user=tweet.user.screen_name,
            status_id=tweet.id)

    print "latest tweet id: %d" %latest_tweet_processed
    
    return {
      #only count tweets with images
      "numberTweets":numberTweets,
      "tweetsSent":tweetsSent,
      "tweetsNotSent":tweetsNotSent,
      "latest_tweet_id":latest_tweet_processed
      }

def getPhotoUrlFromTweet(tweet):
  
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

def readTweetEntities(tweetid):
  print "********Reading Tweet********"
  api = prepareTweetyAPI()
  tweet = api.get_status(tweetid)
  print tweet_actions.isReplyingToMe(tweet)
  return tweet._json