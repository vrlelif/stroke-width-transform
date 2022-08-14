from matplotlib import pyplot as plt
from StrokeWidthTransform import SWT_apply
from connectedComponent import CC
from findLetterCandidates import findLetterCandidates
from readImage import Read
from groupingLetters import *
import timeit
import numpy as np

imagePath = "images/800px-Text_on_a_coach.jpg"
'''getting original image'''
originalImage = Read.getImage(imagePath)
'''getting image as grayscale'''
grayImage = Read.getImageAsGrayScale(imagePath)
'''calculating gradient directions'''
gradientDirections = Read.getGradientDirections(grayImage) 
'''detecting edge pixels'''
edgeImage = Read.get_edges(grayImage) 

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

starttime = timeit.default_timer()
pairs = findPairs(components)

print("findPairs done in:", timeit.default_timer() - starttime)

starttime = timeit.default_timer()

groups = groupG(pairs)

print(groups)

print("groupPairs done in:", timeit.default_timer() - starttime)

imgplot2 = plt.imshow(component_map)
plt.show()
