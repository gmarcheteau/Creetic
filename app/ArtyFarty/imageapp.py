import clustercolors
import processimage
import drawing
import numpy as np
import bsgenerator as bs
import bsgenerator_en as bs_en
import random

from config import MIN_CLUSTERS,MAX_CLUSTERS, DEFAULT_URLS

def commentOnImage(url):
  
  if not url:
    return "Hmm, I need an image to comment on, sorry."
  else:
    ##url_to_image(url) returns both small version (to be clustered) and bigger (to be re-drawn)
    processed_image = processimage.url_to_image(url)
    image_resized = processed_image["smaller_imagefromurl"]
    image_original_size = processed_image["imagefromurl"]
    #get image sized
    width, height = image_resized.size
    width_original, height_original = image_original_size.size
    
    print "MIN_CLUSTERS: %s" %str(MIN_CLUSTERS)
    print "MAX_CLUSTERS: %s" %str(MAX_CLUSTERS)
    clust = clustercolors.fitColorClustering(
      image_resized=image_resized,
      image_original_size=image_original_size,
      min_clusters=MIN_CLUSTERS,
      max_clusters=MAX_CLUSTERS
      )
    
    #get values from clustering
    clt = clust["clt"]
    score = clust["score"]
    simpler_image_array = clust["simpler_image_array"]
    
    maincolors = clustercolors.getColorsFromClusters(clt)
    comment = bs_en.generatePhrase(maincolors)
    
    #colorBoxes
    colorboxes = drawing.drawColorBoxes(maincolors)
    
    #simplerImage
    simplerimage = drawing.drawSimplerImage(
      simpler_image_array = simpler_image_array,
      #simpler_image_array = image_array,
      width = width_original,
      height = height_original
      )
    
    #transform to strings for easier use in html template
    score = ("{0:.0f}".format(score))
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
    response["score"] = score
    response["colorboxes"] = colorboxes
    response["simplerimage"] = simplerimage
  
    return response

def commentOnImageFullMode(url,number_iter=1,SHOW_SIMPLER_IMAGES=False):
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
 
  #default url is invalid or no input
  if (len(url)<2):
    url="http://www.fondationlouisvuitton.fr/content/flvinternet/fr/expositions/exposition-les-clefs-d-une-passion/la-danse-d-henri-matisse/_jcr_content/content/columncontrol_8b3e/leftG6/image_2398.flvcrop.980.5000.jpeg"
