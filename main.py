from matplotlib import pyplot as plt
from StrokeWidthTransform import SWT_apply
from connectedComponent import CC
from readImage import Read
import timeit

imagePath = "../scene3/lfsosa_12.08.2002/IMG_2482.JPG"

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

result , components, featureList  = CC(SWTResult,originalImage)

print("CC done in:", timeit.default_timer() - starttime)

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
imgplot2 = plt.imshow(result)
plt.show()





