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
from flask import request,make_response,render_template,redirect,url_for

from app import app
from forms import URLForm


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
  comment = bs_en.generatePhrase()
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
  
  #number of clustering versions to show
  number_iter = request.args.get('iter', default=1)
  
  #get data from image comment (comment, colors, drawn colors)
  imageresponse = imageapp.commentOnImage(imageurl)
  imagecomment = imageresponse["comment"]
  maincolors = imageresponse["maincolors"]
  silhouettescore = imageresponse["silhouettescore"]
  colorboxes = drawColorBoxes(maincolors)
  
  #transform to strings for easier use in html template
  silhouettescore = ("{0:.2f}".format(silhouettescore))
  maincolorstrings = []
  for color in maincolors:
    maincolorstrings.append(
      (
      str(color[0]),
      str(color[1]),
      "{0:.0f}%".format(color[2] * 100)
      )
    )
    
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
                form = form)

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
  
  #get data from image comment (comment, colors, drawn colors)
  #imageresponse = imageapp.commentOnImage(imageurl)
  imageresponse = imageapp.commentOnImageFullMode(imageurl,number_iter)
  imagecomment = imageresponse["comment"]
  maincolors = imageresponse["maincolors"]
  silhouettescores = imageresponse["silhouettescores"]
  
  #define strings and colorboxes as lists to allow showing several version
  colorboxes = []
  maincolorstringslist = []
  for i,colorset in enumerate(maincolors):
    #transform to strings for easier use in html template
    tmpcolorlist = []
    for color in colorset:
      tmpcolorlist.append(
        (
        str(color[0]),
        str(color[1]),
        "{0:.0f}%".format(color[2] * 100)
        )
      )
    maincolorstringslist.append(tmpcolorlist)
    #draw all versions of color boxes
    colorboxes.append(drawColorBoxes(colorset))
    silhouettescores[i] = ("{0:.2f}".format(silhouettescores[i]))
  
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
                form = form)

@app.route('/getbs_img_url', methods=["GET", "POST"])
def getURL():
    form = URLForm()
    if form.validate_on_submit():
        # [...]

        print "input URL: %s" %form.url.data
        return redirect(url_for('getBS_img',imageurl = form.url.data))
    return render_template('login.html', form=form)