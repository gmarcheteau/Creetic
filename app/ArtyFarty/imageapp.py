import clustercolors
import colornames
import processimage
import bsgenerator as bs
import bsgenerator_en as bs_en

def commentOnImage(*url):
  if not url:
    return "Hmm, I need an image to comment on, sorry."
  else:
    #optional URL parameter arrives as a tuple?
    url = url[0]
    image_resized = processimage.url_to_image(url)
    clt = clustercolors.fitColorClustering(image_resized)
    maincolors = clustercolors.getColorsFromClusters(clt)
    #clustercolors.showColorClusters(image_resized,maincolors)
    #save the color boxes as a colorboxes.png
    clustercolors.saveColorBox(maincolors)
    response = {}
    response["comment"] = bs_en.generatePhrase(maincolors)
    response["colors"] = maincolors
    return response

def getURLfromUser():
  #get from user
  url = raw_input("Image URL: ")
  #"http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"
  
  #default url is invalid or no input
  if (len(url)<2):
    url="http://www.fondationlouisvuitton.fr/content/flvinternet/fr/expositions/exposition-les-clefs-d-une-passion/la-danse-d-henri-matisse/_jcr_content/content/columncontrol_8b3e/leftG6/image_2398.flvcrop.980.5000.jpeg"