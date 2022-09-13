import numpy as np
from readImage import *
from findLetterCandidates import *
import numpy as np

imagePath = "images/scene3/lfsosa_12.08.2002/IMG_2471.JPG"
#imagePath = "scene2/ryoungt_05.08.2002/PICT0017.JPG" 
'''getting original image'''
originalImage = getImage(imagePath)
'''getting image as grayscale'''
grayImage =getImageAsGrayScale(imagePath)
'''calculating gradient directions'''
gradientDirections =getGradientDirections(grayImage) 
'''detecting edge pixels'''
edgeImage = get_edges_Otsu(grayImage) 

direction = 1


def SWT_apply_parallel(arr):
    copy_SW_Map = np.copy(initialize_SW_Map(edgeImage))
    start , end =  arr[0], arr[len(arr)-1]

    parallelEdgeImage = edgeImage[start:end]
    parallelGradientDirections = gradientDirections[start:end]
    # parallelSW_Map = SW_Map[start:end]
    
    edgePointRows, edgePointCols =  np.nonzero(parallelEdgeImage) 

    rays = [] 

    for pos in list(zip(edgePointRows,edgePointCols)):

        startGradient = parallelGradientDirections[pos]  

        startX = np.cos(startGradient)
        startY = np.sin(startGradient)

        steps = 1

        ray = [(pos)]
        
        while  True: # TODO:  FIND A VALUE TO LIMIT STROKE WIDTH
            x_q = np.int32(round(pos[1] + (direction * startX * steps)))
            y_q = np.int32(round((pos[0]+start) + (direction * startY * steps)))

            steps = steps + 1

            if not (0 <= x_q < edgeImage.shape[1] and 0 <= y_q < edgeImage.shape[0]):
                break
            
            ray.append((y_q, x_q))

            if edgeImage[y_q, x_q] > 0:
    
                strokeW = np.sqrt( (x_q - pos[1]) ** 2 + (y_q -( pos[0]+start)) ** 2)

                theta = np.abs(np.abs(startGradient - gradientDirections[y_q, x_q]) - np.pi)

                if theta <= np.pi / 2:
                    for ry, rx in ray:
                        copy_SW_Map[ry, rx] = min(copy_SW_Map[ry, rx], strokeW)
                    rays.append(ray) 
                break
            
                
    for ray in rays:
        counter = 0
        median = np.median([copy_SW_Map[y, x] for (y, x) in ray])
        for (y, x) in ray:
            try:
                leftN = copy_SW_Map[y,x-1]
                aboveN = copy_SW_Map[y-1,x]
                bottomN = copy_SW_Map[y+1,x] 
                rightN = copy_SW_Map[y,x+1]

                if len([i for i in [leftN,aboveN,bottomN,rightN] if i== float("inf")]) >= 2:
                    counter = counter + 1
            except IndexError:
                continue
        if counter < len(ray)/2:
            for (y, x) in ray:
                copy_SW_Map[y, x] = min(median, copy_SW_Map[y, x])
                #pass
        else:
            for (y, x) in ray:
                copy_SW_Map[y, x] = float("inf")            

 

    return copy_SW_Map[start:end]


    


 


