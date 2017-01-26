#!/usr/bin/env python
import tweet_processor
import os, sys

########
#try and find latest tweet processed
try:
  filename = "latest_tweet_id.txt"
  file = open(filename, "r")
  LATEST_TWEET_PROCESSED = int(file.read())
  file.close()
except Exception as err:
  print "Error opening %s -- %s" %(filename,str(err))

tweet_processor.checkTweetsAndReply(LATEST_TWEET_PROCESSED)



