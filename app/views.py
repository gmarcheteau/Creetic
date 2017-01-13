#!/usr/bin/env python

import urllib
import json
import os
import matplotlib.pyplot as plt
import ArtyFarty.bsgenerator as bs
import ArtyFarty.bsgenerator_en as bs_en
import ArtyFarty.drawing as drawing
import ArtyFarty.imageapp as imageapp
import StringIO
from rq import Queue
from worker import conn

from flask import Flask
from flask import request,make_response,render_template,redirect,url_for

from app import app
from forms import URLForm

q = Queue(connection=conn)

@app.route('/getbs', methods=['GET'])
def getBS():
  comment = bs.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/news', methods=['GET'])
def goNews():
  return render_template("news.html")

@app.route('/')
@app.route('/getbs_en', methods=['GET'])
def getBS_en():
  #comment = bs_en.generatePhrase()
  comment = imageresponse = q.enqueue(bs_en.generatePhrase)
  return render_template("getbs.html",comment=comment)


@app.route('/getbs_img', methods=['GET','POST'])
def getBS_img():
  import base64
  
  defaultURL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"
  
  imageurl = request.args.get('imageurl', default=defaultURL)
  #remove quotes in url if any
  imageurl = imageurl.strip('"').strip('\'')
  if not imageurl.startswith("http"):
    imageurl = defaultURL
  
  #number of clusters to use --TODO: do something with it
  number_clusters = request.args.get('clusters', default=5)
  
  #get data from image comment (comment, colors, drawn colors)
  #NEED TO enqueue blocking function
  #imageresponse = imageapp.commentOnImage(imageurl)
  imageresponse = q.enqueue(imageapp.commentOnImage(imageurl), 'http://heroku.com')
  
  imagecomment = imageresponse["comment"]
  maincolorstrings = imageresponse["maincolorstrings"]
  silhouettescore = imageresponse["silhouettescore"]
  colorboxes = imageresponse["colorboxes"]
  simplerimage = imageresponse["simplerimage"]
  
  form = URLForm()
  if form.validate_on_submit():
    # [...]
    print "input URL: %s" %form.url.data
    return redirect(url_for('getBS_img',imageurl = form.url.data))
  
  return render_template("getbs_img.html",
                imagecomment = imagecomment,
                imageurl = imageurl,
                maincolorstrings = maincolorstrings,
                silhouettescore = silhouettescore,
                colorboxes = colorboxes,
                simplerimage = simplerimage,
                form = form)

@app.route('/getbs_img_multi', methods=['GET','POST'])
def getBS_img_multi():
  import base64
  
  defaultURL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"
  
  imageurl = request.args.get('imageurl', default=defaultURL)
  #remove quotes in url if any
  imageurl = imageurl.strip('"').strip('\'')
  if not imageurl.startswith("http"):
    imageurl = defaultURL
  
  #number of clustering versions to show
  number_iter = request.args.get('iter', default=5, type=int)
  
  #SHOW_SIMPLER_IMAGES config from url
  SHOW_SIMPLER_IMAGES = request.args.get('show_simpler_images', default=False, type=bool)
  print "SHOW_SIMPLER_IMAGES --", str(SHOW_SIMPLER_IMAGES)
  
  #get data from image comment (comment, colors, drawn colors)
  #imageresponse = imageapp.commentOnImage(imageurl)
  imageresponse = imageapp.commentOnImageFullMode(imageurl,number_iter,SHOW_SIMPLER_IMAGES)
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