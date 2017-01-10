import clustercolors
import colornames
import processimage
import drawing
import bsgenerator as bs
import bsgenerator_en as bs_en
import random

defaultURL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"

MIN_CLUSTERS=2
MAX_CLUSTERS=6


def commentOnImage(url=defaultURL):
  
  if not url:
    return "Hmm, I need an image to comment on, sorry."
  else:
    image_resized = processimage.url_to_image(url)
    
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

def commentOnImageFullMode(url=defaultURL,number_iter=1):
  maincolors =[]
  silhouettescores = []
  if not url:
    return "Hmm, I need an image to comment on, sorry."
  else:
    #optional URL parameter arrives as a tuple?
    url = url
    image_resized = processimage.url_to_image(url)
    
    for i in range(0,number_iter):
      clust = clustercolors.fitColorClustering(
      image_resized,
      min_clusters=i+2,
      max_clusters=i+2
      )
      clt = clust["clt"]
      silhouette = clust["silhouette"]
      #add maincolors from this iteration to list
      maincolors.append(clustercolors.getColorsFromClusters(clt))
      #add silhouette score for this iteration to list
      silhouettescores.append(silhouette)
      
    #comment on one of the versions (random)
    rand = random.randint(0,len(maincolors)-1)
    comment = bs_en.generatePhrase(maincolors[rand])
    response = {}
    response["comment"] = comment
    response["maincolors"] = maincolors
    response["silhouettescores"] = silhouettescores
    return response

def getURLfromUser():
  #get from user
  url = raw_input("Image URL: ")
  #"http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"
  
  #default url is invalid or no input
  if (len(url)<2):
    url="http://www.fondationlouisvuitton.fr/content/flvinternet/fr/expositions/exposition-les-clefs-d-une-passion/la-danse-d-henri-matisse/_jcr_content/content/columncontrol_8b3e/leftG6/image_2398.flvcrop.980.5000.jpeg"