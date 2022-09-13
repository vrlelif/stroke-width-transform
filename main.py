from findLetterCandidates import *
from masking import masking
import matplotlib.pyplot as plt
import timeit
from strokeWidthTransform import SWT_apply
#from newStrokeWidthTransform import SWT_apply_new
from newStrokeWidthTransformParallel import * 
from  readImage import *
from multiprocessing import Pool
#from parallelSWT import *

if __name__ == "__main__":

    processesCount = 10 # DECLARE NUMBER OF PROCESSORS
    p = Pool(processes = processesCount)   # CREATE POOL
    height = originalImage.shape[0] # GET THE HEIGHT OF THE IMAGE
    ranges = [] # CREATE AN EMPTY ARRAY TO FILL WITH ROW SLICES FOR EACH PROCESSOR

    for i in range(processesCount): # CREATE AND APPEND RANGES
        steps = i*int(height/processesCount)
        myRange = range(steps,steps+int(height/processesCount)+1) 
        ranges.append(myRange)

    slices = p.map(SWT_apply_parallel,ranges) # CALL THE PROCESSORS 

    #SWTMap = np.sum(slices, axis=0) 


    SWTMap = np.concatenate(slices, axis=0) 


    '''
    SWTMap = SWT_apply_new(edgeImage, SW_Map, gradientDirections , direction = direction)
    print("SWT:", timeit.default_timer() - starttime)

    '''
    component_map , components  = CC(SWT=SWTMap,direction=direction,originalImage=originalImage)
    
    component_map , components = findLetterCandidates(component_map , components, SWTMap, originalImage)   # CALL FIND LETTER CANDIDATES





    masked = masking(components,originalImage)

    plt.figure()
    plt.imshow(masked[...,::-1])
    plt.show()


    