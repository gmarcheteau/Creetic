##LOAD AND RESIZE AN IMAGE FROM URL##
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import urllib
import time as t
from PIL import Image
import requests
from StringIO import StringIO


def url_to_image(url):
  response = requests.get(url)
  imagefromurl = Image.open(StringIO(response.content))
  #plt.imshow(imagefromurl)
  #plt.show()
  
  # Resize image
  h, w = imagefromurl.size
  w_new = int(100 * w / max(w, h) )
  h_new = int(100 * h / max(w, h) )
  
  maxsize = (w_new, h_new)
  imagefromurl.thumbnail(maxsize, Image.ANTIALIAS)
  #plt.imshow(image_resized)
  #plt.show()
  
  return imagefromurl