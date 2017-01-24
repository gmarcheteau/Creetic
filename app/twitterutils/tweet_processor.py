#!/usr/bin/env python
import tweepy
import socket
import requests
import time
from authentication import authentication
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ArtyFarty import bsgenerator_en as bs_en

#adapted from http://piratefache.ch/twitter-streaming-api-with-tweepy/

###
#tweet_data = json.loads(tweet)  # This allows the JSON data be
###

class TwitterStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are t received from the stream.
    """

    def on_status(self, status):
        #print "tweet"
        #get_text(status)
        get_user_mentions(status)
        get_hashtags(status)
        #sendBSTweet(status.id, status.user.screen_name)

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes

    def on_error(self, status_code):
        if status_code == 403:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False

def get_text(tweet):
  print("Tweet Message : " + tweet.text)
  #print("Tweet Favorited \t:" + str(tweet.favorited))
  #print("Tweet Favorited count \t:" + str(tweet.favorite_count))
    
def get_hashtags(tweet):
  # Display hashtags
  if tweet.entities["hashtags"]:
    print "Hashtags:"
    for hashtag in tweet.entities["hashtags"]:
      print '#%s' %hashtag["text"]

def get_user_mentions(tweet):
  # Display user mentions
  if tweet.entities["user_mentions"]:
    print "User mentions:"
    for user_mention in tweet.entities["user_mentions"]:
      print '@%s' %user_mention["screen_name"]


def sendCommentLink(api, picurl, to_user,status_id):
  commenturl = buildCommentURL(picurl)
  to_user = '@'+to_user
  
  text = to_user
  text += " "
  text += "Here's what @ArtyFarty7 thinks about your pic:"
  text += " "
  text += commenturl
  
  print "----sending tweet----"
  print text
  print to_user
  print status_id
  print "in reply to tweet %d" %status_id
  
  try:
    #LIKE THE TWEET
    api.create_favorite(status_id)
    #SEND A REPLY
    api.update_status(status=text,in_reply_to_status_id=status_id)
    #api.update_status(status="tweet in response to %d" %status_id)
    return "ok"
  except Exception as err:
    print "Error calling api -- %s" %str(err)
    return "Error calling api -- %s" %str(err)

def sendBSTweet(api,to_user,status_id):
  to_user = '@'+to_user
  
  #TODO BETTER -- only generate short BS texts
  bstext = bs_en.generatePhrase()
  counter = 1
  print "Generated BS #%d" %counter
  print "Length: %d" %len(bstext)
  
  while len(bstext)>116:
    counter += 1
    bstext = bs_en.generatePhrase()
    #print "Generated BS #%d" %counter
    #print "Length: %d" %len(bstext)
  
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

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

    '''
    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
    myStream.filter(track=['#ArtyFartyPlease'], async=True)
    '''
    
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
            commenturl = buildCommentURL(picurl)
            print "picture in tweet: %s" %picurl
            print "comment available on: %s" %commenturl
            
            #REPLY AND ADD STATUS TO PARAMETERS
            process_response = []
            process_response += sendCommentLink(
              api=api,
              picurl=picurl,
              to_user=tweet.user.screen_name,
              status_id=tweet.id)
            
            process_responses.append((
              str(tweet.created_at),
              tweet.user.screen_name,
              process_response
              ))
          else:
            print "media is not a photo"
      else:
        print "no media url found"
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