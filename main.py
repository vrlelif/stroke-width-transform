from matplotlib import pyplot as plt
from strokeWidthTransform import SWT_apply
from connectedComponent import CC
from findLetterCandidates import findLetterCandidates
from readImage import Read
#from parallelSWT import SWT_apply
from groupingLetters import *
import timeit
import cv2 
import numpy as np
import matplotlib.patches as patches

if __name__ == '__main__':
    starttime2 = timeit.default_timer()


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

    component_map , components  = CC(SWTResult)

    print("CC done in:", timeit.default_timer() - starttime)

    starttime = timeit.default_timer()

    component_map , components = findLetterCandidates(component_map , components, SWTResult, originalImage)  

    print("findLetterCandidates done in:", timeit.default_timer() - starttime)

    starttime = timeit.default_timer()
    pairs = findPairs(components)

    print("findPairs done in:", timeit.default_timer() - starttime)

    starttime = timeit.default_timer()

    groups = groupG(pairs)


    print("groupPairs done in:", timeit.default_timer() - starttime)

    final_image = np.zeros(component_map.shape)

    for group in groups:
        for item in group:
            labels = np.argwhere(component_map == item)
            final_image[labels[:, 0], labels[:, 1]] = 1

    def bbox1(img):
        a = np.where(img != 0)
        return [np.min(a[1]),np.min(a[0]) , np.max(a[1])-np.min(a[1]),np.max(a[0])-np.min(a[0])]


    bb = bbox1(final_image)
    '''
    f = plt.figure()
    f.add_subplot(1,2, 1)
    plt.imshow(cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB))
    f.add_subplot(1,2, 2)
    plt.imshow(cv2.cvtColor(edgeImage, cv2.COLOR_BGR2RGB))
    plt.show(block=True)
    '''



    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB))
    #ax.imshow(component_map)


    rect = patches.Rectangle((bb[0], bb[1]), bb[2], bb[3], linewidth=1, edgecolor='r', facecolor='none')

    # Add the bb to the Axes
    ax.add_patch(rect)
    print(f"Total TIME FOR {originalImage.shape[0]} x {originalImage.shape[1]} is { timeit.default_timer() - starttime2}" )


    plt.show()


