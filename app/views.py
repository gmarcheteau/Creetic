#!/usr/bin/env python

import urllib
import json
import os
import time
import random
import matplotlib.pyplot as plt
import ArtyFarty.bsgenerator as bs
import ArtyFarty.bsgenerator_en as bs_en
import ArtyFarty.drawing as drawing
import ArtyFarty.imageapp as imageapp
import ArtyFarty.sendemail as sendemail
import ArtyFarty.receivemail as receivemail
import twitterutils.tweet_in as tweet_in
import twitterutils.tweet_out as tweet_out
import StringIO
import resource
import redis
from rq import Queue
from rq.job import Job
from worker import conn

from flask import Flask
from flask import request,make_response,render_template,redirect,url_for

from app import app

from forms import URLForm

from config import DEFAULT_URLS

q = Queue(connection=conn)

@app.route('/getbs', methods=['GET'])
def getBS():
  comment = bs.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/news', methods=['GET'])
def goNews():
  return render_template("news.html")

@app.route('/getbs_en', methods=['GET'])
def getBS_en():
  comment = bs_en.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/', methods=['GET','POST'])
@app.route('/getbs_img', methods=['GET','POST'])
def getBS_img():
  defaultURL=chooseDefaultURLfromList()
  imageurl = request.args.get('imageurl', default=defaultURL)
  #remove quotes in url if any
  imageurl = imageurl.strip('"').strip('\'')
  if not imageurl.startswith("http"):
    imageurl = "http:\\"+imageurl
  
  #number of clusters to use --TODO: do something with it
  number_clusters = request.args.get('clusters', default=5)
  
  form = URLForm()
  if form.validate_on_submit():
    # [...]
    print "input URL: %s" %form.url.data
    try:
      return redirect(url_for('getBS_img',imageurl = form.url.data))
    except Exception as err:
      print "error in form bit -- %s" %str(err)
  
  ##CALL TEMPLATE WITH JUST AVAILABLE DATA##
  ##The page then call /startimageanalysis to start the job and /result to update##
  return render_template(
    'getbs_img2.html',imageurl=imageurl,form=form)
  
  '''
  return render_template("getbs_img.html",
                imagecomment = imageBS["imagecomment"],
                imageurl = imageBS["imageurl"],
                maincolorstrings = imageBS["maincolorstrings"],
                score = imageBS["score"],
                colorboxes = imageBS["colorboxes"],
                simplerimage = imageBS["simplerimage"],
                form = form)
  '''
  
def produceImageBS(imageurl):
  import base64
  
  #if receiving a local image, add full path
  if not imageurl.startswith("http"):
    print "appending full path to url"
    imageurl = os.path.abspath(imageurl)
  
  #get data from image comment (comment, colors, drawn colors)
  
  imageresponse = imageapp.commentOnImage(imageurl)
  
  print '(from views.py) Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  
  imagecomment = imageresponse["comment"]
  maincolorstrings = imageresponse["maincolorstrings"]
  score = imageresponse["score"]
  colorboxes = imageresponse["colorboxes"]
  simplerimage = imageresponse["simplerimage"]
  
  #return dict with all values to generate HTML response
  #provides ability to choose template independently
  return {
    "status" : "success",
    "imagecomment" : imagecomment,
    "imageurl" : imageurl,
    "maincolorstrings" : maincolorstrings,
    "score" : score,
    "colorboxes" : colorboxes,
    "simplerimage" : simplerimage
    }

@app.route('/getbs_img_multi', methods=['GET','POST'])
def getBS_img_multi():
  import base64
  defaultURL=chooseDefaultURLfromList()
  imageurl = request.args.get('imageurl', default=defaultURL)
  #remove quotes in url if any
  imageurl = imageurl.strip('"').strip('\'')
  if not imageurl.startswith("http"):
    imageurl = "http:\\"+imageurl
  
  #number of clustering versions to show
  number_iter = request.args.get('iter', default=5, type=int)
  
  #SHOW_SIMPLER_IMAGES config from url
  SHOW_SIMPLER_IMAGES = request.args.get('show_simpler_images', default=False, type=bool)
  print "SHOW_SIMPLER_IMAGES --", str(SHOW_SIMPLER_IMAGES)
  
  #get data from image comment (comment, colors, drawn colors)
  #imageresponse = imageapp.commentOnImageFullMode(imageurl,number_iter,SHOW_SIMPLER_IMAGES)
  #REDIS enqueue blocking function
  #imageresponse = imageapp.commentOnImage(imageurl)

  job = q.enqueue(
    imageapp.commentOnImageFullMode,
    imageurl,number_iter,SHOW_SIMPLER_IMAGES
    )
  # TODO: how long to wait?
  while not job.result:
    imageresponse = ''
  imageresponse = job.result
  
  imagecomment = imageresponse["comment"]
  maincolorstringslist = imageresponse["maincolorstringslist"]
  silhouettescores = imageresponse["silhouettescores"]
  colorboxes = imageresponse["colorboxes"]
  simplerimages = imageresponse["simplerimages"]
  
  print "len(simplerimages):", len(simplerimages)
  
  print silhouettescores
  print len(silhouettescores)
  
  form = URLForm()
  if form.validate_on_submit():
    # [...]
    print "input URL: %s" %form.url.data
    return redirect(url_for('getBS_img_multi',imageurl = form.url.data))
  
  return render_template("getbs_img_multi.html",
                imagecomment = imagecomment,
                imageurl = imageurl,
                maincolorstringslist = maincolorstringslist,
                silhouettescores = silhouettescores,
                colorboxes = colorboxes,
                simplerimages = simplerimages,
                SHOW_SIMPLER_IMAGES = SHOW_SIMPLER_IMAGES,
                form = form)

@app.route('/getbs_img_url', methods=["GET", "POST"])
def getURL():
    form = URLForm()
    if form.validate_on_submit():
        # [...]

        print "input URL: %s" %form.url.data
        return redirect(url_for('getBS_img',imageurl = form.url.data))
    return render_template('enterurl.html', form=form)

@app.route('/checkmail', methods=['GET','POST'])
def checkmail():
 
  newMessages = receivemail.checkNewMailWithImages()
  for message in newMessages:
    imageurl = os.path.abspath(message["imageurl"])
    print "imageurl sent to generator: %s" %imageurl
    sendMailAboutImage(
      imageurl=imageurl,
      toaddr=message["fromaddr"])
  return "<h2>Found and analysed %d image(s)</h2>" %len(newMessages)
  

defaulttoaddr = "gregoire.marcheteau@gmail.com"
def sendMailAboutImage(imageurl,toaddr=defaulttoaddr):
  #toaddr = request.args.get('email', default=defaulttoaddr)
  
  #imageBS is a dict with all you need to create the HTML resp
  imageBS = produceImageBS(imageurl)
  
  htmlmessage = render_template("getbs_img_mail.html",
                imagecomment = imageBS["imagecomment"],
                imageurl = "http://localhostimage"+imageBS["imageurl"],
                maincolorstrings = imageBS["maincolorstrings"],
                score = imageBS["score"],
                colorboxes = imageBS["colorboxes"],
                simplerimage = imageBS["simplerimage"],
                form = imageBS["form"])
  print "http://localhostimage"+imageBS["imageurl"]
  sendemail.sendEmail(htmlmessage,toaddr)
  
@app.route('/setlatesttweetIN/<latesttweetid>', methods=['GET','POST'])
def overrideLatestTweetIN(latesttweetid):
  #FORCE OVERRIDE?
  sudo = request.args.get('sudo', default=0, type=int)
  
  response = ''
  latesttweetid = int(latesttweetid)
  
  #get value from Redis
  try:
    LATEST_TWEET_REDIS = int(conn.get('LATEST_TWEET_IN_PROCESSED'))
    print "Reading from Redis - LATEST_TWEET_IN_PROCESSED: %d" %LATEST_TWEET_REDIS
    
    if latesttweetid > LATEST_TWEET_REDIS or sudo == 1:
      #set value to Redis
      conn.set('LATEST_TWEET_IN_PROCESSED',latesttweetid)
      response += "OK -- set %d as latest tweet IN on Redis"%latesttweetid
    else:
      response += "Equally or more recent tweet IN found on Redis: %d" %LATEST_TWEET_REDIS
  
  #if couldn't find latest tweet, set it anyway
  except Exception as err:
    conn.set('LATEST_TWEET_IN_PROCESSED',latesttweetid)
    response += "Couldn't retrieve latest tweet IN from Redis -- %s" %str(err)
    response += "<hr>"
    response += "Set %d as latest tweet IN on Redis"%latesttweetid
  
  return response

@app.route('/setlatesttweetOUT/<latesttweetid>', methods=['GET','POST'])
def overrideLatestTweetOUT(latesttweetid):
  #FORCE OVERRIDE?
  sudo = request.args.get('sudo', default=0, type=int)
  
  response = ''
  latesttweetid = int(latesttweetid)
  
  #get value from Redis
  try:
    LATEST_TWEET_REDIS = int(conn.get('LATEST_TWEET_OUT_PROCESSED'))
    print "Reading from Redis - LATEST_TWEET_OUT_PROCESSED: %d" %LATEST_TWEET_REDIS
    
    if latesttweetid > LATEST_TWEET_REDIS or sudo == 1:
      #set value to Redis
      conn.set('LATEST_TWEET_OUT_PROCESSED',latesttweetid)
      response += "OK -- set %d as latest tweet OUT on Redis"%latesttweetid
    else:
      response += "Equally or more recent tweet OUT found on Redis: %d" %LATEST_TWEET_REDIS
  
  #if couldn't find latest tweet, set it anyway
  except Exception as err:
    conn.set('LATEST_TWEET_OUT_PROCESSED',latesttweetid)
    response += "Couldn't retrieve latest tweet OUT from Redis -- %s" %str(err)
    response += "<hr>"
    response += "Set %d as latest tweet OUT on Redis"%latesttweetid
  
  return response

@app.route('/tweetin', methods=['POST','GET'])
def tweetIn():
  #get latest tweet from Redis
  LATEST_TWEET_PROCESSED = getLatestTweetInFromRedis()
  
  if (LATEST_TWEET_PROCESSED):
    #check for new tweets and process them (e.g. save and reply)
    twitter_response = tweet_in.checkTweetsAndReply(LATEST_TWEET_PROCESSED)
  
  #update latest tweet to Redis
  setLatestTweetInToRedis(twitter_response["latest_tweet_id"])
  
  return json.dumps(
    twitter_response,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
    )

@app.route('/tweetout', methods=['POST'])
def tweetOut():
  #get latest tweet from Redis
  LATEST_TWEET_PROCESSED = getLatestTweetOutFromRedis()
  
  if (LATEST_TWEET_PROCESSED):
    #check for new tweets and process them (e.g. save and reply)
    twitter_response = tweet_out.foundTweetsToReplyTo(LATEST_TWEET_PROCESSED)
  
  #update latest tweet to Redis
  setLatestTweetOutToRedis(twitter_response["latest_tweet_id"])
  
  return json.dumps(
    twitter_response,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
    )


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)
    
    if job.is_failed:
      print "Failed"
      return "Failed", 404
    
    elif job.is_finished:
        imageBS = job.result
        #JSONIFY
        imageBS = json.dumps(imageBS, ensure_ascii=False)
        return imageBS, 200

    else:
        print "Nay! 202"
        return "Not yet!", 202

@app.route('/startimageanalysis', methods=['POST'])
def get_img_analysis():
  # get imageurl
  data = json.loads(request.data.decode())
  imageurl = data["imageurl"]
  
  #REDIS enqueue function
  job = q.enqueue_call(
    func=produceImageBS, args=(imageurl,), result_ttl=5000
    )
  print "JOB ID:",job.get_id()
  print "Image URL: ",imageurl
  return job.get_id()

@app.route('/testtwitter', methods=['POST','GET'])
def testtwitter():
  return test_twitter.tweetBirdyImage()

def chooseDefaultURLfromList():
  rand = random.randint(0,len(DEFAULT_URLS)-1)
  return DEFAULT_URLS[rand]
  
def getLatestTweetInFromRedis():
  #get values from Redis
  try:
    LATEST_TWEET_IN_PROCESSED = int(conn.get('LATEST_TWEET_IN_PROCESSED'))
    print "Reading from Redis - LATEST_TWEET_IN_PROCESSED: %d" %LATEST_TWEET_IN_PROCESSED
    return LATEST_TWEET_IN_PROCESSED
  except Exception as err:
    print "Unable to retrieve latest tweet IN from Redis -- %s" %str(err)
    return None
  
def getLatestTweetOutFromRedis():
  #get values from Redis
  try:
    LATEST_TWEET_OUT_PROCESSED = int(conn.get('LATEST_TWEET_OUT_PROCESSED'))
    print "Reading from Redis - LATEST_TWEET_OUT_PROCESSED: %d" %LATEST_TWEET_OUT_PROCESSED
    return LATEST_TWEET_OUT_PROCESSED
  except Exception as err:
    print "Unable to retrieve latest tweet OUT from Redis -- %s" %str(err)
    return None

  
def setLatestTweetInToRedis(latesttweetid):
  try:
    conn.set('LATEST_TWEET_IN_PROCESSED',latesttweetid)
    print "Writing to Redis - LATEST_TWEET_IN_PROCESSED: %d" %latesttweetid
    return None
  except Exception as err:
    print "Unable to set latest tweet IN to Redis -- %s" %str(err)
    return None
  
def setLatestTweetOutToRedis(latesttweetid):
  try:
    conn.set('LATEST_TWEET_OUT_PROCESSED',latesttweetid)
    print "Writing to Redis - LATEST_TWEET_OUT_PROCESSED: %d" %latesttweetid
    return None
  except Exception as err:
    print "Unable to set latest tweet OUT to Redis -- %s" %str(err)
    return None

@app.route("/manualtweetout/<tweetid>", methods=['POST'])
def manualTweetOut(tweetid):
  return json.dumps(
    tweet_out.manualTweetReply(tweetid),
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
    )
