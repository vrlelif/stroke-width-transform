from matplotlib import pyplot as plt
from StrokeWidthTransform import SWT_apply
from connectedComponent import CC
from readImage import Read
import timeit
import numpy as np


imagePath = "images/1200px-Text_on_a_coach.jpg"

'''getting original image'''
originalImage = Read.getImage(imagePath)

'''getting image as grayscale'''
grayImage = Read.getImageAsGrayScale(imagePath)

'''calculating gradient directions'''
gradientDirections = Read.getGradientDirections(grayImage) 

'''detecting edge pixels'''
edgeImage = Read.get_edges(grayImage) # get edges of image

starttime = timeit.default_timer()

SW_Map = Read.initialize_SW_Map(edgeImage)

SWTResult = SWT_apply(edgeImage,SW_Map,gradientDirections)

print("SWT done in :", timeit.default_timer() - starttime)

starttime = timeit.default_timer()

component_map , components  = CC(SWTResult,originalImage)

print("CC done in:", timeit.default_timer() - starttime)


def findLetterCandidate(component_map, components):

    newResult  =  np.zeros(component_map.shape)

    for component in list(components):

        c = np.unique(components[component], axis=0)

        '''calculate variance rate'''
        arrS = [SWTResult[p[0], p[1]] for p in c]
        
        arrY = sorted(c, key=lambda x: x[0])
        arrX = sorted(c, key=lambda x: x[1])

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
        
        uniqueArr = np.unique(component_map[minY:minY+height, minX:minX+width])

        '''CONDITIONS'''
        varianceRatio = (varianceV/averageV) <= 2 
        aspectRatio = 0.1 <= aspect <= 10
        diameterRatio = (median / diameter) <= 15.00
        heightV = 10 <= height <= 300
        widthV =  10 <= width <= 300
        compCount = len(uniqueArr[uniqueArr != 0]) <=3


        if varianceRatio and aspectRatio and diameterRatio and heightV and widthV and compCount:
            #result = cv2.rectangle(result, (minX,minY ), (minX + width ,minY+height), (255,0,255), 1)
            for p in components[component]:
                newResult[p[0],p[1]] = component

            arrY = sorted(components[component], key=lambda x: x[0])
            arrX = sorted(components[component], key=lambda x: x[1])

            minY  =  arrY[0][0]
            maxY  =  arrY[len(arrY) - 1 ][0]
            minX  =  arrX[0][1] #hsv
            maxX  =  arrX[len(arrX) - 1 ][1]

            height = maxY - minY + 1
            width = maxX - minX + 1

            comp = originalImage[minY:minY+height, minX:minX+width]
        
            avg_color_per_row = np.average(comp[newResult[minY:minY+height, minX:minX+width]> 0],axis=0)

            avg_color = np.average(avg_color_per_row, axis=0)

            #componentFeatureList[component] = [median, height, minX, maxX, avg_color]
        
        

                
    return newResult, components,

component_map ,components = findLetterCandidate(component_map , components)  

'''
pairs = []

for i in featureList:
    c = filter(lambda x: ((featureList[x][0] /featureList[i][0])<2 
    and (featureList[x][1] /featureList[i][1])<2 ) and (featureList[x][2] == featureList[i][2] ), featureList)
    if len(list(c))>0 :
        featureList

    pairs.append(list(c))

'''



#result = np.float32(newResult)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
imgplot2 = plt.imshow(component_map)
plt.show()





