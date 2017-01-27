#!/usr/bin/env python
import tinyurl
import tweepy
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ArtyFarty import bsgenerator_en as bs_en

def replyToTweet(api, to_user,status_id,picurl):
  if picurl:
    text = prepareText(picurl)
  else:
    text = prepareText()
  
  print "----sending tweet----"
  print text
  print "to user @%s" %to_user
  print "in reply to tweet %d" %status_id
  
  try:
    api.create_favorite(status_id) #LIKE THE TWEET
    api.create_friendship(to_user) #CREATE FRIENDSHIP
  except Exception as err:
    print "error with liking or friending -- %s" %str(err)
  
  try: #SEND A REPLY
    api.update_status(
      status=text,
      in_reply_to_status_id=status_id,
      auto_populate_reply_metadata=True)
    return "OK"

  except Exception as err:
    traceback.print_exc()
    print "error in posting -- %s" %str(err)
    return "Error calling api -- %s" %str(err)
  
def prepareText(*picurl):
  text = ''
  
  if picurl:
    picurl = picurl[0]
    commenturl = buildCommentURL(picurl)
    commenturl = tinyurl.create_one(commenturl) #tiny url for comment link --19 char
    text += ' '
    text += commenturl
    
  else:
    text += ' '
    text += 'goo.gl/AegUWZ'
  
  text = bs_en.generatePhrase_short(140-len(text)) + text
  return text
    
def buildCommentURL(picurl):
  baseurl = "http://artyfarty.herokuapp.com/getbs_img?imageurl="
  return baseurl+picurl+':medium'