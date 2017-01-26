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

def sendCommentLink(api, picurl, to_user,status_id):
  commenturl = buildCommentURL(picurl)
  #tiny url for comment link
  commenturl = tinyurl.create_one(commenturl)
  text =''
  #text += '@'+to_user
  #text += " "
  text += bs_en.generatePhrase_short(113)
  text += " "
  text += commenturl
  
  print "----sending tweet----"
  print text
  print "to user @%s" %to_user
  print "in reply to tweet %d" %status_id
  
  try:
    #LIKE THE TWEET
    api.create_favorite(status_id)
    #CREATE FRIENDSHIP
    api.create_friendship(to_user)
  except Exception as err:
    print "error with liking and friending -- %s" %str(err)
  
  try:
    #SEND A REPLY
    api.update_status(
      status=text,
      in_reply_to_status_id=status_id,
      auto_populate_reply_metadata=True)
    #api.update_status(status="tweet in response to %d" %status_id)
    return "ok"
  except Exception as err:
    traceback.print_exc()
    print "error in posting -- %s" %str(err)
    return "Error calling api -- %s" %str(err)

def sendBSTweet(api,to_user,status_id):
  to_user = '@'+to_user
  
  #TODO BETTER? -- only generate short BS texts
  bstext = bs_en.generatePhrase_short(limit=116)
  
  text = to_user
  text += ' '
  text += bstext
  text += ' '
  text += 'goo.gl/AegUWZ'
  text += ' '
  text += '#ArtyFarty'
  
  print text
  print to_user
  print status_id
  print "in reply to tweet %d" %status_id
  
  try:
    api.update_status(status=text,in_reply_to_status_id=status_id)
    #api.update_status(status="tweet in response to %d" %status_id)
    return "ok"
  except Exception as err:
    print "Error calling api -- %s" %str(err)
    return str(err)
  

def checkTweetsAndReply(latest_tweet_processed):

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

    #since_id -- need to store latest tweet in order to not respond multiple times
    
    tweets = api.search(
      q = "#ArtyFartyPlease",
      since_id=latest_tweet_processed,
      include_entities=True)
    
    ##save all to file tweets.txt
    text_file = open("tweets.txt", "a")
    
    print "Number of tweets found: %d" %len(tweets)
    process_responses = []
    
    for tweet in tweets:
      #write to file
      text_file.write('\n')
      text_file.write('\n')
      text_file.write("date: %s" %str(tweet.created_at))
      text_file.write('\n')
      text_file.write("tweet id: %s" %str(tweet.id))
      text_file.write('\n')
      text_file.write("user: %s" %str(tweet.user.screen_name))
      text_file.write('\n')
      text_file.write("tweet: %s" %tweet.text.encode("utf-8"))
      
      #update latest tweet id
      if tweet.id>latest_tweet_processed:
        latest_tweet_processed = tweet.id
        
      #CHECK IF TWEET HAS MEDIA URL
      if "media" in tweet.entities and tweet.entities['media'][0]['media_url']:
        for media in tweet.entities['media']:
          #CHECK IF MEDIA IS PHOTO
          if media["type"]=="photo":
            print str(media)
            #got media_url - means add it to the output
            picurl = media['media_url']
            print "picture in tweet: %s" %picurl
            
            #REPLY AND ADD STATUS TO PARAMETERS
            process_response = []
            process_response += sendCommentLink(
              api=api,
              picurl=picurl,
              to_user=tweet.user.screen_name,
              status_id=int(tweet.id))
            
            process_responses.append((
              str(tweet.created_at),
              tweet.user.screen_name,
              process_response
              ))
          else:
            print "media is not a photo"
            
      else:
        print "no media url found"
        #SEND TWEET WITH JUST BS TEXT
        process_response = []
        process_response += sendBSTweet(
          api=api,
          to_user=tweet.user.screen_name,
          status_id=tweet.id)
        
        process_responses.append((
          str(tweet.created_at),
          tweet.user.screen_name,
          process_response
          ))
        pass
    
    text_file.close()
  
    #save latest tweet_id to file latest_tweet_id.txt
    text_file2 = open("latest_tweet_id.txt", "w")
    text_file2.write('%d' %latest_tweet_processed)
    text_file2.close()
  
    print "latest tweet id: %d" %latest_tweet_processed
    
    return {
      #only count tweets with images
      "number_tweets":len(process_responses),
      "process_responses":process_responses
      }

def buildCommentURL(picurl):
  baseurl = "http://artyfarty.herokuapp.com/getbs_img?imageurl="
  return baseurl+picurl+':medium'