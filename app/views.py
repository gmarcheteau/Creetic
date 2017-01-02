#!/usr/bin/env python

import urllib
import json
import os
import matplotlib.pyplot as plt
import ArtyFarty.bsgenerator as bs
import ArtyFarty.bsgenerator_en as bs_en
import ArtyFarty.imageapp as imageapp
import StringIO

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from app import app


@app.route('/getbs', methods=['GET'])
def getBS():
  comment = bs.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/')
@app.route('/getbs_en', methods=['GET'])
def getBS_en():
  comment = bs_en.generatePhrase()
  return render_template("getbs.html",comment=comment)

@app.route('/getbs_img', methods=['GET'])
def getBS_img():
  import base64
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
  #colorboxes = imageresponse["colorboxes"]
  
  colorboxes = drawColorBoxes(maincolors)
  
  return render_template("getbs_img.html",
                imagecomment = imagecomment,
                imageurl = imageurl,
                colorboxes = colorboxes)
  

def drawColorBoxes(maincolors):
  import base64
  from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
  from matplotlib.figure import Figure
  #plot color graph
  lastX=0
  for i in maincolors:
    plt.axvspan(lastX, lastX+i[2], edgecolor='none', facecolor=i[1], alpha=1)
    lastX+=i[2]
  plt.xlim(0, 1)
  plt.axis('off')
  
  fig = plt.gcf()
  fig.set_facecolor('none')
  fig.savefig('./app/static/images/colorboxes.png', dpi=30, transparent=True)
  
  canvas=FigureCanvas(fig)
  png_output = StringIO.StringIO()
  canvas.print_png(png_output)
  colorboxes = base64.b64encode(png_output.getvalue())
  return colorboxes

