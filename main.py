from startProcess import startProcess
from findLetterCandidates import findLetterCandidates
from masking import masking
import matplotlib.pyplot as plt


import timeit
import cv2 


if __name__ == "__main__":

    imagePath = "images/tiny.jpg"
    originalImage = cv2.imread(imagePath,cv2.COLOR_BGR2RGB)

    SWTMap, component_map, components = startProcess(originalImage)
    
    component_map , components = findLetterCandidates(component_map , components, SWTMap, originalImage)   # CALL FIND LETTER CANDIDATES

    result = masking(component_map,components,originalImage)

    plt.figure()
    plt.imshow(result[...,::-1])
    plt.show()

 
    #cv2.imshow("fdgdfg",originalImage)
    #cv2.waitKey(0)

 
