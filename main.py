from matplotlib import pyplot as plt
from strokeWidthTransform import SWT_apply
from connectedComponent import CC
from findLetterCandidates import findLetterCandidates
from readImage import Read
from parallelSWT import SWT_apply_parallel
from parallelSWT import *
from groupingLetters import *
from multiprocessing import Pool
import timeit
import cv2 
import numpy as np
import matplotlib.patches as patches
if __name__ == "__main__":

    beginningTime = timeit.default_timer() #  LAUNCH TIMER

    processesCount = 10 # DECLARE NUMBER OF PROCESSORS

    p = Pool(processes = processesCount)   # CREATE POOL

    height = originalImage.shape[0] # GET THE HEIGHT OF THE IMAGE

    ranges = [] # CREATE AN EMPTY ARRAY TO FILL WITH ROW SLICES FOR EACH PROCESSOR

    for i in range(processesCount): # CREATE AND APPEND RANGES
        steps = i*int(height/processesCount)
        myRange = range(steps,steps+int(height/processesCount)+1) 
        ranges.append(myRange)


    slices = p.map(SWT_apply_parallel,ranges) # CALL THE PROCESSORS 
    
    SWTResult = np.concatenate(slices, axis=0) # MERGE THE RESULTS AND GET WHOLE IMAGE
    #SWTResult = SWT_apply(edgeImage, SW_Map, gradientDirections , direction = 1) # MERGE THE RESULTS AND GET WHOLE IMAGE

    print("SWT done in :", timeit.default_timer() - beginningTime) # PRINT SWT RUNNING TIME

    starttime = timeit.default_timer() # LAUNCH THE TIMER

    component_map , components  = CC(SWTResult) # CALL THE CONNECTED COMPONENT

    print("CC done in:", timeit.default_timer() - starttime) #PRINT CONNECTED COMPONENT RUNNING TIME

    starttime = timeit.default_timer() # LAUNCH THE TIMER

    component_map , components = findLetterCandidates(component_map , components, SWTResult, originalImage)   # CALL FIND LETTER CANDIDATES

    print("findLetterCandidates done in:", timeit.default_timer() - starttime)# PRINT FIND LETTER CANDIDATES RUNNING TIME

    starttime = timeit.default_timer()  # LAUNCH THE TIMER

    pairs = findPairs(components) # CALL THE findPairs

    print("findPairs done in:", timeit.default_timer() - starttime)

    starttime = timeit.default_timer()  # LAUNCH THE TIMER

    groups = groupG(pairs) # CALL THE groupG

    print("groupPairs done in:", timeit.default_timer() - starttime)# PRINT groupG RUNNING TIME

    final_image = np.zeros(component_map.shape)


    lines = []

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

        image = cv2.rectangle(originalImage, a, b, color=(255,255,255), thickness=2)  
    
    '''
    f = plt.figure()
    f.add_subplot(1,2, 1)
    plt.imshow(cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB))
    f.add_subplot(1,2, 2)
    plt.imshow(cv2.cvtColor(edgeImage, cv2.COLOR_BGR2RGB))
    plt.show(block=True)
    '''
    image = cv2.rectangle(originalImage, a, b, color=(255, 0, 0), thickness=2)  
    cv2.imshow("fdgdfg",image)
    cv2.waitKey(0)

    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB))
    #ax.imshow(component_map)
    '''
    rect = patches.Rectangle((bb[0], bb[1]), bb[2], bb[3], linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    print(f"Total TIME FOR {originalImage.shape[0]} x {originalImage.shape[1]} is { timeit.default_timer() - beginningTime} with {processesCount} processors" )

    plt.show()
    '''

