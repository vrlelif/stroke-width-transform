import cv2  # openCV
import numpy as np  # numpy library to be able to play with arrays
from matplotlib import pyplot as plt
from StrokeWidthTransform import SWT_apply
from connectedComponent import CC
import timeit

def getImage(path):  # get image and read it as RGB
    image = cv2.imread(path)
    return image

def getImageAsGrayScale(path):  # get image and read it as grayscale
    image = cv2.imread(path, 0)
    return image

def get_edges(im, lo: float = 200, hi: float = 300, window: int = 3):
    edges = cv2.Canny(im, lo, hi, apertureSize=window)
    return edges
    
def getGradientDirections(image): #get gradient directions
    gradientX = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1,dy=0, ksize=-1) #get x gradient
    gradientY = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0,dy=1, ksize=-1) #get y gradient
    return np.arctan2(gradientY, gradientX) # get gradient directions and return an image

def initialize_SW_Map(edgeImage):
    SW_Map = np.matrix(np.ones(edgeImage.shape) * np.inf)
    return SW_Map

imagePath = "../scene3/lfsosa_12.08.2002/IMG_2490.JPG"

#imagePath = "images/800px-Text_on_a_coach.jpg"
#imagePath = "images/whyHurry.jpg"

'''getting original image'''
originalImage = getImage(imagePath)

'''getting image as grayscale'''
grayImage = getImageAsGrayScale(imagePath)

'''calculating gradient directions'''
gradientDirections = getGradientDirections(grayImage) 
'''detecting edge pixels'''
edgeImage = get_edges(grayImage) # get edges of image

starttime = timeit.default_timer()

SW_Map = initialize_SW_Map(edgeImage)

SWTResult = SWT_apply(edgeImage,SW_Map,gradientDirections)

print("SWT done in :", timeit.default_timer() - starttime)

starttime = timeit.default_timer()

result, eq_list , components  = CC(SWTResult)

print("CC done in:", timeit.default_timer() - starttime)

#result = np.float32(newResult)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
imgplot2 = plt.imshow(result)
plt.show()





