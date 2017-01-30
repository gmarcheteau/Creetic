#!/usr/bin/env python
import base64
import StringIO
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from PIL import Image

def drawColorBoxes(maincolors):
  #plot color graph
  lastX=0
  for i in maincolors:
    #normalize rgb color to 0-1 range
    print "facecolor: %s" %str(i[0])
    norm = Normalize(vmin=0.,vmax=250.)
    facecolor=(norm(i[0][0]),norm(i[0][1]),norm(i[0][2]))
    print "normalized facecolor: %s" %str(facecolor)
    plt.axvspan(lastX, lastX+i[2], edgecolor='none', facecolor=facecolor, alpha=1)
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

def drawSimplerImage(simpler_image_array,width,height):
  
  #reshape the array to the image form factor
  reshaped_array = np.reshape(simpler_image_array,(width,3*height))
  
  img = Image.new( 'RGB', (width,height), "black") # create a new black image
  pixels = img.load() # create the pixel map
  
  for i in range(width):    # for every pixel:
    for j in range(height):
        pixels[i,j] = (
          reshaped_array[i,3*j],
          reshaped_array[i,3*j+1],
          reshaped_array[i,3*j+2]
          )
          
  #increase size of image with size_factor (~resolution)
  #resized_pixels = extendArraySize(pixels,size_factor)
  
  # Resize image -- make it bigger this time (previously max=100)
  size_factor = 3
  (w_new, h_new)=(size_factor*width,size_factor*height)
  img = img.resize((w_new, h_new))
  
  print "Original size: %s x %s" %(width,height)
  print "New size: %s x %s" %(w_new, h_new)
  
  png_output = StringIO.StringIO()
  img.save(png_output, format="PNG")
  simpler_image = base64.b64encode(png_output.getvalue())
  png_output.close()
  return simpler_image

def extendArraySize(array,size_factor):
  (width,height)=array.shape
  newarray = np.zeros((size_factor*width,size_factor*height),dtype=np.int)
  for i in range(width):
    for j in range(height):
      #print array[i,j]*np.ones((size_factor,size_factor))
      for k in range(size_factor):
        for l in range(size_factor):
          newarray[size_factor*i+k,size_factor*j+l]=array[i,j]
  return newarray

def extendListSize(list,size_factor):
  newlist=[]
  for item in list:
      for k in range(size_factor):
        for l in range(size_factor):
          newlist.append(item)
  return newlist