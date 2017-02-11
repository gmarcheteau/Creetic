#!/usr/bin/env python
import tinyurl
import tweepy
import sys,os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ArtyFarty import bsgenerator_en as bs_en
from ArtyFarty import imageapp
from config import TWITTER_ON


def replyToTweet(api,to_user,status_id):
  text = prepareText()
  
  print "----sending tweet----(%s)" %TWITTER_ON
  print text
  print "to user @%s" %to_user
  print "in reply to tweet %d" %status_id
  
  if(TWITTER_ON):
    try: #SEND A REPLY
      api.update_status(
        status=text,
        in_reply_to_status_id=status_id,
        auto_populate_reply_metadata=True)
      api.create_favorite(status_id) #LIKE THE TWEET
      api.create_friendship(to_user) #CREATE FRIENDSHIP
      return "OK"
  
    except Exception as err:
      #traceback.print_exc()
      print "error in posting -- %s" %str(err)
      return "Error calling api -- %s" %str(err)
  else:
    print "Testing (not sent)"
    return "Testing (not sent)"
  
def prepareText(*picurl):
  text = ''
  
  if picurl:
    
    #randomly send or not link to comment on site (will have less space for BS on tweet)
    if random.randint(1,3)%3 == 0:
      SEND_LINK_TO_COMMENT=False
    else:
      SEND_LINK_TO_COMMENT=True
    
    if(SEND_LINK_TO_COMMENT):
      picurl = picurl[0]
      commenturl = buildCommentURL(picurl)
      commenturl = tinyurl.create_one(commenturl) #tiny url for comment link --19 char
      text += ' '
      text += commenturl
    
    text += ' #Creetic'
    
  else:
    text += ' '
    text += 'creetic.io'
  
  available_length = 140-len(text)
  print "Available length for BS: %d" %available_length
  
  text = bs_en.generatePhrase_short(available_length) + text
  return text
    
def buildCommentURL(picurl):
  baseurl = "http://www.creetic.io/getbs_img?imageurl="
  return baseurl+picurl+':medium'

#SAVE SIMPLER IMAGE TO FILE, TO BE TWEETED
def saveSimplerImage(simplerimage,filename):
  # Do something smart with charset and b64 instead of assuming
  simplerimage = simplerimage.decode("base64")
  
  # Do something smart with mime_type
  with open(filename, 'wb') as f:
      f.write(simplerimage)

def replyToTweetWithSimplerImage(api,to_user,status_id,picurl):
  
  message = prepareText(picurl)
  print "----sending tweet----(%s)" %TWITTER_ON
  print message
  print "to user @%s" %to_user
  print "in reply to tweet %d" %status_id
  
  if(TWITTER_ON):
    try:
      filename = 'temp.png'
      
      simplerimage = imageapp.commentOnImage(picurl)["simplerimage"]
      saveSimplerImage(simplerimage,filename)
      
      print "sending tweet %s to %s" %(message,to_user)
      
      api.update_with_media(
        filename=filename,
        status=message,
        in_reply_to_status_id=status_id,
        auto_populate_reply_metadata=True)
      
      api.create_favorite(status_id) #LIKE THE TWEET
      api.create_friendship(to_user) #CREATE FRIENDSHIP
      
      return "Tweet sent"
    
    except Exception as err:
      print str(err)
      return str(err)
  else:
    print "Testing (not sent)"
    return "Testing (not sent)"
    