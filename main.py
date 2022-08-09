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

imagePath = "images/hull.jpeg"

#imagePath = "images/Capture.PNG"
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

print("The time difference is :", timeit.default_timer() - starttime)

starttime = timeit.default_timer()

result, eq_list , components  = CC(SWTResult)

print("The time difference is :", timeit.default_timer() - starttime)

newResult  =  np.zeros(result.shape)

for component in list(components):
    '''calculate variance rate'''
    arrS = [SWTResult[p[0], p[1]] for p in components[component]]
    
    arrY = sorted(components[component], key=lambda x: x[0])
    arrX = sorted(components[component], key=lambda x: x[1])

    minY  =  arrY[0][0]
    maxY  =  arrY[len(arrY) - 1 ][0]
    minX  =  arrX[0][1]
    maxX  =  arrX[len(arrX) - 1 ][1]

    height = maxY - minY + 1
    width = maxX - minX + 1

    aspect = width  / height

    varianceV = np.var(arrS)
    averageV = np.mean(arrS)
    
    median = np.median(arrS)
    diameter = np.sqrt( height ** 2 + width ** 2)


    '''CONDITIONS'''
    varianceRatio = (varianceV/averageV) <= 2 
    aspectRatio = 0.1 <= aspect <= 10
    diameterRatio = (median / diameter) <= 10.00
    

    heightV = 10 <= height <= 300
    widthV =  10 <= width <= 300
    
    uniqueArr = np.unique(result[minY:maxY, minX:maxX])

    compCount = len(uniqueArr[uniqueArr != 0])


    if varianceRatio and aspectRatio and diameterRatio and heightV and widthV and compCount <=3:
        #result = cv2.rectangle(result, (minX,minY ), (minX + width ,minY+height), (255,0,255), 1)

        for p in components[eq_list[component]]:
            newResult[p[0],p[1]] = eq_list[component]


#cv2.imshow("result",result)
#cv2.waitKey(0)

result = np.float32(newResult)
result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

imgplot2 = plt.imshow(result)
plt.show()



