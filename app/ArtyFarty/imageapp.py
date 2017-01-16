import clustercolors
import colornames
import processimage
import drawing
import numpy as np
import bsgenerator as bs
import bsgenerator_en as bs_en
import random

defaultURL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"

MIN_CLUSTERS=3
MAX_CLUSTERS=5


def commentOnImage(url=defaultURL,*number_clusters):
  
  if not url:
    return "Hmm, I need an image to comment on, sorry."
  else:
    image_resized = processimage.url_to_image(url)
    
    #if number_clusters specified, use only that
    if number_clusters:
      MIN_CLUSTERS = number_clusters[0]
      MAX_CLUSTERS = MIN_CLUSTERS
    
    clust = clustercolors.fitColorClustering(
      image_resized,
      min_clusters=MIN_CLUSTERS,
      max_clusters=MAX_CLUSTERS
      )
    
    #get values from clustering
    clt = clust["clt"]
    silhouettescore = clust["silhouette"]
    simpler_image_array = clust["simpler_image_array"]
    width, height = image_resized.size
    
    maincolors = clustercolors.getColorsFromClusters(clt)
    comment = bs_en.generatePhrase(maincolors)
    
    #colorBoxes
    colorboxes = drawing.drawColorBoxes(maincolors)
    
    #simplerImage
    simplerimage = drawing.drawSimplerImage(
      simpler_image_array = simpler_image_array,
      #simpler_image_array = image_array,
      width = width,
      height = height
      )
    
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
    
    #build response
    response = {}
    response["comment"] = comment
    response["maincolorstrings"] = maincolorstrings
    response["silhouettescore"] = silhouettescore
    response["colorboxes"] = colorboxes
    response["simplerimage"] = simplerimage
  
    return response

def commentOnImageFullMode(url=defaultURL,number_iter=1,SHOW_SIMPLER_IMAGES=False):
  maincolors =[]
  silhouettescores = []
  simplerimages = []
  
  if not url:
    return "Hmm, I need an image to comment on, sorry."
  else:
    #optional URL parameter arrives as a tuple?
    url = url
    image_resized = processimage.url_to_image(url)
    width, height = image_resized.size
    
    #build the datasets for each cluster iteration
    for i in range(0,number_iter):
      clust = clustercolors.fitColorClustering(
      image_resized,
      min_clusters=i+2,
      max_clusters=i+2
      )
      clt = clust["clt"]
      silhouette = clust["silhouette"]
      simpler_image_array = clust["simpler_image_array"]
      
      #add maincolors from this iteration to list
      maincolors.append(clustercolors.getColorsFromClusters(clt))
      #add silhouette score for this iteration to list
      silhouettescores.append(silhouette)
      
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
        colorboxes.append(drawing.drawColorBoxes(colorset))
        silhouettescores[i] = ("{0:.2f}".format(float(silhouettescores[i])))
      
      #add simpler image for this iteration
      if(SHOW_SIMPLER_IMAGES):
        simplerimages.append(drawing.drawSimplerImage(
           simpler_image_array = simpler_image_array,
           #simpler_image_array = image_array,
           width = width,
           height = height
           ))
    
    #comment on one of the versions (random)
    rand = random.randint(0,len(maincolors)-1)
    comment = bs_en.generatePhrase(maincolors[rand])
    
    #build response
    response = {}
    response["comment"] = comment
    response["maincolorstringslist"] = maincolorstringslist
    response["colorboxes"] = colorboxes
    response["silhouettescores"] = silhouettescores
    response["simplerimages"] = simplerimages
    return response

def getURLfromUser():
  #get from user
  url = raw_input("Image URL: ")
  #"http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"
  
  #default url is invalid or no input
  if (len(url)<2):
    url="http://www.fondationlouisvuitton.fr/content/flvinternet/fr/expositions/exposition-les-clefs-d-une-passion/la-danse-d-henri-matisse/_jcr_content/content/columncontrol_8b3e/leftG6/image_2398.flvcrop.980.5000.jpeg"
