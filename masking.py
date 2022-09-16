from groupingLettersIntoTextLines import groupingLettersIntoTextLines
import numpy as np
import cv2 
import timeit


def masking(components, originalImage):


    groups = groupingLettersIntoTextLines(components)

    points = []

    arr = []

    if len(groups)>0:
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
            
            print(f"X= {a[0]} , Y= {a[1]} , WIDTH= {b[0]-a[0]+1}, HEIGHT= {b[1]-a[1]+1}")


            result = cv2.rectangle(originalImage, a, b, color=(0,255,0), thickness=2)  


            arr.append(result)

    else:
        result = originalImage 
        arr.append(result)


        
    return result
