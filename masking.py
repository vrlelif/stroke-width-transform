from groupingLetters import groupingLettersIntoTextLines
import numpy as np
from PIL import Image
import cv2 
from parallelSWT import edgeImage


def masking(component_map, components, originalImage):

    groups = groupingLettersIntoTextLines(components)

    final_image = np.zeros(component_map.shape)

    points = []

    for group in groups:

        minimumXs = []
        minimumYs = []
        maximumXs = []
        maximumYs = []

        for el in group:
            minimumXs.append(components[el]['minX'])
            minimumYs.append(components[el]['minY'])
            maximumXs.append(components[el]['maxX'])
            maximumYs.append(components[el]['maxY'])

        a = min(minimumXs),min(minimumYs)
        b = max(maximumXs),max(maximumYs)

        im = Image.fromarray(component_map)

        result = cv2.rectangle(originalImage, a, b, color=(0,0,255), thickness=2)  
        #contours, hierarchy = cv2.findContours(image=edgeImage, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        #result = cv2.drawContours(image=originalImage.copy(), contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    return result 
