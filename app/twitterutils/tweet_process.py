#!/usr/bin/env python
import tinyurl
import tweepy
import sys,os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ArtyFarty import bsgenerator_en as bs_en
from ArtyFarty import imageapp
from config import TWITTER_ON,MY_TWITTER_ID
from config import TWITTER_CHARACTER_LIMIT

def isReplyingToMe(tweet): ##TODO: check if reply to multiple users, maybe does not catch it
    if tweet.in_reply_to_user_id_str == str(MY_TWITTER_ID):
        print "REPLYING TO ME"
    else:
        print "NOT REPLYING TO ME"
    return tweet.in_reply_to_user_id_str == str(MY_TWITTER_ID)