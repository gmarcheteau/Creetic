import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import colornames
import base64
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score, pairwise_distances
 
##FLATTEN AND CLUSTER USING K-MEANS##
def fitColorClustering(image_resized,min_clusters,max_clusters):
  
  # Reshape the image to be a list of pixels
  width, height = image_resized.size
  #image_array = np.array(list(image_resized.getdata()))
  image_array = np.reshape(image_resized,(width*height,3),order='F')

  ##Evaluate clustering with Silhouette coefficient, and select best (from 2 to 10 clusters)
  bestScore = -1
  bestClusters = 0;
  scores = []
  response = {}
  
  for clusters in range(min_clusters, max_clusters+1):
      # Cluster colours
      clt = KMeans(n_clusters = clusters)
      clt.fit(image_array)
  
      # Validate clustering result
      ##DEBUGGING: removing calculation of silhouette score, replacing by dummy###
      #silhouette = silhouette_score(image_array, clt.labels_, metric='euclidean')
      score = calinski_harabaz_score(image_array, clt.labels_) 
      scores.append(score)
      
      #Print intermediate evals
      print "With",clusters,"clusters:"
      print "Score:",score
  
      # Find the best one
      if score > bestScore:
          bestScore = score;
          bestClusters = clusters;
      
      #override number of clusters
      #bestClusters = MAX_CLUSTERS
      
  print "Optimized clustering:"
  print bestClusters,"clusters"
  print "Score:",bestScore
  
  # Cluster colours with optimized parameters
  clt = KMeans(n_clusters = bestClusters)
  clt.fit(image_array)
  response["clt"] = clt
  response["simpler_image_array"] = getClusterForEachPixel(image_array,clt)
  
  return response


##SORT CLUSTERS BY SIZE##
# By Adrian Rosebrock
def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)
 
    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
 
    # return the histogram
    return hist

#extract color centers and names from clustering
def getColorsFromClusters(clt):
  # Finds how many pixels are in each cluster
  hist = centroid_histogram(clt)
  
  # Sort the clusters according to how many pixel they have
  zipped = zip (hist, clt.cluster_centers_)
  zipped.sort(reverse=True, key=lambda x : x[0])
  hist, clt.cluster_centers = zip(*zipped)
  
  maincolors = []
  
  for i in zipped:
      print "Weight:","{0:.0f}%".format(i[0] * 100)
      rgbcolor=np.uint8(i[1])
      colorname=colornames.get_colour_name(rgbcolor)[1]
      print "RGB color:",rgbcolor
      print "Color name:",colorname
      
      #build list with main colors, names and weights
      rgbcolortuple=(rgbcolor[0],rgbcolor[1],rgbcolor[2])
      maincolors.append((rgbcolortuple,str(colorname),i[0]))
  
  return maincolors

#maincolors is the output from the clustering, in a list
def showColorClusters(image_resized,maincolors):
  #plt.imshow(image_resized)
  #plt.show()
  image_resized.rotate(0).show()
  
  #plot color graph
  lastX=0
  for i in maincolors:
    plt.axvspan(lastX, lastX+i[2], edgecolor='none', facecolor=i[1], alpha=1)
    lastX+=i[2]
  plt.xlim(0, 1)
  plt.axis('off')
  plt.show()

#maincolors is the output from the clustering, in a list
def drawColorBoxes(maincolors):
  from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
  from matplotlib.figure import Figure
  import StringIO
  #plot color graph
  lastX=0
  for i in maincolors:
    plt.axvspan(lastX, lastX+i[2], edgecolor='none', facecolor=i[1], alpha=1)
    lastX+=i[2]
  plt.xlim(0, 1)
  plt.axis('off')
  
  fig = plt.gcf()
  canvas=FigureCanvas(fig)
  png_output = StringIO.StringIO()
  canvas.print_png(png_output)
  colorboxes = base64.b64encode(png_output.getvalue())
  return colorboxes
  
  #fig.savefig('./app/static/images/colorboxes.png', dpi=30)
  #canvas=FigureCanvas(fig)
  #png_output = StringIO.StringIO()
  #canvas.print_png(png_output)

#list of all pixels with corresponding cluster
def getClusterForEachPixel(image_array,clt):
  simpler_image_array = []
  clusterized_array = clt.predict(image_array)
  
  for cluster_number in clusterized_array:
    cluster_rgb = clt.cluster_centers_[cluster_number]
    #build tuple
    cluster_rgb=np.uint8(cluster_rgb)
    cluster_rgb_tuple=(cluster_rgb[0],cluster_rgb[1],cluster_rgb[2])
    simpler_image_array.append(cluster_rgb_tuple)
  return simpler_image_array
    
