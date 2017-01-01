#!/usr/bin/env python

import urllib
import json
import os
import ArtyFarty.bsgenerator as bs
import ArtyFarty.bsgenerator_en as bs_en
import ArtyFarty.imageapp as imageapp

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from app import app

@app.route('/tuto')
def index():
    user = {'nickname': 'Greg'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/getbs', methods=['GET'])
def getBS():
  comment = bs.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/getbs_en', methods=['GET'])
def getBS_en():
  comment = bs_en.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/getbs_img', methods=['GET'])
def getBS_img():
  imageurl = request.args.get('imageurl')
  defaultURL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"
  if not imageurl:
    imageurl = defaultURL
  #remove quotes in url if any
  imageurl = imageurl.strip('"').strip('\'')
  if not imageurl.startswith("http"):
    imageurl = defaultURL
  
  #get data from image comment (comment, colors, drawn colors)
  imageresponse = imageapp.commentOnImage(imageurl)
  imagecomment = imageresponse["comment"]
  maincolors = imageresponse["colors"]
  print type(imageresponse)
  print type(imagecomment)
  print type(maincolors)
  
  return render_template("getbs_img.html",
                imagecomment = imagecomment,
                imageurl = imageurl,
                colorboxesurl = "./static/images/colorboxes.png")
  
  #response += "<div style=\"width:500px;height:100px;border:0px solid #000;background-color:rgb"+str(maincolors[0][0])+";\">Main color</div>"
  
  #TODO: getting image from local, saved in clustercolors.py, not working.
  #response += "<img src=\"colorboxes.png\" alt=\"main colors\" />"

@app.route("/simple.png")
def simple():
    import datetime
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


