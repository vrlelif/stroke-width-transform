from matplotlib import pyplot as plt
from StrokeWidthTransform import SWT_apply
from connectedComponent import CC
from findLetterCandidates import findLetterCandidates
from readImage import Read
import timeit
import numpy as np


imagePath = "images/tiny.jpg"

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

starttime = timeit.default_timer()

component_map , components = findLetterCandidates(component_map , components, SWTResult, originalImage)  

print("findLetterCandidates done in:", timeit.default_timer() - starttime)

def findPairs(components):
    pairs = []

    for co in components:
        for can in components:
            if co == can or co > can:
                continue
            widerCompWidth = min(components[co]['width'],components[can]['width'])
            strokeM = components[co]['medianS'] / components[can]['medianS']  <= 2
            heights = components[co]['height'] / components[can]['height']  <= 2
            distance = components[co]['maxX'] - components[can]['minX'] < 3 * widerCompWidth
            colors = np.mean(components[co]['avgColor']) / np.mean(components[can]['avgColor']) <= 3 
            if (strokeM and heights and distance and colors):
                pairs.append([co,can])

    return pairs

starttime = timeit.default_timer()
pairs = findPairs(components)
print("findPairs done in:", timeit.default_timer() - starttime)

print(pairs)

# def groupG(pairs):
#     lenBefore = len(pairs)
#     groups = []
#     if len(pairs) > 1:
#         for i,pair in enumerate(pairs):
#             try:
#                 if (any(point in pairs[i+1] for point in pair)):
#                     group = np.concatenate(( pair,  pairs[i+1]))
#                     group = np.unique(group)
#                     groups.append(group)

#             except IndexError:
#                 continue
#         if len(groups) < lenBefore:
#             return groupG(groups)
#         else: 
#             return groups
#     else:
#         return pairs


print(groupG(pairs))





    
    
#result = np.float32(newResult)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

imgplot2 = plt.imshow(component_map)
plt.show()
