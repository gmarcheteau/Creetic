##LOAD AND RESIZE AN IMAGE FROM URL##
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import urllib
import resource
import time as t
from PIL import Image
import requests
from StringIO import StringIO

def url_to_image(url):
  
  #original size image (keep it to then re-draw it)
  imagefromurl = Image.open(StringIO(urllib.urlopen(url).read()))
  #copy and resize (smaller version to be clustered)
  smaller_imagefromurl = imagefromurl
  
  # Resize image
  w, h = imagefromurl.size
  w_new = int(100 * w / max(w, h) )
  h_new = int(100 * h / max(w, h) )
  
  print "Original size: %s x %s" %(w,h)
  print "New size: %s x %s" %(w_new, h_new)
  
  maxsize = (w_new, h_new)

  smaller_imagefromurl.thumbnail(maxsize, Image.ANTIALIAS)
  print "Thumbnail size: %s" %str(smaller_imagefromurl.size)
  #plt.imshow(image_resized)
  #plt.show()
  
  print '(from processimage.py) Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  
  return {"imagefromurl":imagefromurl,"smaller_imagefromurl":smaller_imagefromurl}


  