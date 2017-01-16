##LOAD AND RESIZE AN IMAGE FROM URL##
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import urllib
import time as t
from PIL import Image
import requests
from StringIO import StringIO
from pympler.tracker import SummaryTracker
tracker = SummaryTracker()


def url_to_image(url):
  
  
  
  #response = requests.get(url,headers={'Connection':'close'})
  #imagefromurl = Image.open(StringIO(response.content))
  imagefromurl = Image.open(StringIO(urllib.urlopen(url).read()))
  #plt.imshow(imagefromurl)
  #plt.show()
  
  # Resize image
  w, h = imagefromurl.size
  w_new = int(100 * w / max(w, h) )
  h_new = int(100 * h / max(w, h) )
  
  print "Original size: %s x %s" %(w,h)
  print "New size: %s x %s" %(w_new, h_new)
  
  maxsize = (w_new, h_new)

  imagefromurl.thumbnail(maxsize, Image.ANTIALIAS)
  print "Thumbnail size: %s" %str(imagefromurl.size)
  #plt.imshow(image_resized)
  #plt.show()
  
  #track memory usage with Pympler
  print "-----Pympler Memory usage (from processimage.py)-----"
  tracker.print_diff()
  
  return imagefromurl
