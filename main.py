from findLetterCandidates import *
from masking import masking
import matplotlib.pyplot as plt
import timeit
from SWT import *
from  readImage import *
from multiprocessing import Pool

if __name__ == "__main__":

    starttime2 = timeit.default_timer()

    SW_Map = initialize_SW_Map(edgeImage)
    SWTMap = SWT_new_normal(edgeImage, SW_Map, gradientDirections , direction = direction)
    print(f"Normal SWT: {timeit.default_timer() - starttime2} for {SWTMap.shape}")


    processesCount = 10 # DECLARE NUMBER OF PROCESSORS
    p = Pool(processes = processesCount)   # CREATE POOL
    height = originalImage.shape[0] # GET THE HEIGHT OF THE IMAGE
    ranges = [] # CREATE AN EMPTY ARRAY TO FILL WITH ROW SLICES FOR EACH PROCESSOR

    for i in range(processesCount): # CREATE AND APPEND RANGES
        steps = i*int(height/processesCount)
        myRange = range(steps,steps+int(height/processesCount)+1) 
        ranges.append(myRange)

    starttime = timeit.default_timer()

    slices = p.map(SWT_new_parallel,ranges) # CALL THE PROCESSORS 

    SWTMap = np.concatenate(slices, axis=0) 

    print(f"Parallel SWT: {timeit.default_timer() - starttime} for {SWTMap.shape}")


    component_map , components  = CC(SWT=SWTMap,direction=direction)
    
    component_map , components = findLetterCandidates(component_map , components, SWTMap, originalImage)   # CALL FIND LETTER CANDIDATES


    masked = masking(components,originalImage)

    plt.figure()
    plt.imshow(masked[...,::-1])
    plt.show()


    