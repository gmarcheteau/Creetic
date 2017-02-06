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
  smaller_imagefromurl = Image.open(StringIO(urllib.urlopen(url).read()))
  
  # Resize smaller image (to be clustered)
  MAX = 100
  w, h = smaller_imagefromurl.size
  w_new = int(MAX * w / max(w, h) )
  h_new = int(MAX * h / max(w, h) )
  
  maxsize = (w_new, h_new)
  smaller_imagefromurl.thumbnail(maxsize, Image.ANTIALIAS)
  
  # Resize original image (to be redrawn)
  MAX_O = 1000
  w_o, h_o = imagefromurl.size
  w_o_new = int(MAX_O * w_o / max(w_o, h_o) )
  h_o_new = int(MAX_O * h_o / max(w_o, h_o) )

  maxsize_o = (w_o_new, h_o_new)
  imagefromurl.thumbnail(maxsize_o, Image.ANTIALIAS)
  
  print "Original size: %s x %s" %(w,h)
  print "New size for clustering: %s x %s" %(w_new, h_new)
  print "New size for redrawing: %s x %s" %(w_o_new, h_o_new)
  
  #print "Thumbnail size: %s" %str(smaller_imagefromurl.size)
  #plt.imshow(image_resized)
  #plt.show()
  
  print '(from processimage.py) Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  
  return {"imagefromurl":imagefromurl,"smaller_imagefromurl":smaller_imagefromurl}


  