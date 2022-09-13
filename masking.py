from groupingLettersIntoTextLines import groupingLettersIntoTextLines
import numpy as np
import cv2 
import timeit


def masking(components, originalImage):

    starttime = timeit.default_timer()


    groups = groupingLettersIntoTextLines(components)

    print("GLITL:", timeit.default_timer() - starttime)


    final_image = np.zeros(originalImage.shape)

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

            #im = Image.fromarray(component_map)

            result = cv2.rectangle(originalImage, a, b, color=(0,255,0), thickness=1)  

            #result = a[0], a[1], b[0]-a[0], b[1]-a[1]+1

            arr.append(result)


            #contours, hierarchy = cv2.findContours(image=edgeImage, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

            #result = cv2.drawContours(image=originalImage.copy(), contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    else:
        result = originalImage 
        #result = 0,0,0,0
        arr.append(result)


        
    return result
