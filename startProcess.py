from multiprocessing import Pool
from parallelSWT import *
from connectedComponent import CC



def startProcess(originalImage):
    
    processesCount = 10 # DECLARE NUMBER OF PROCESSORS
    p = Pool(processes = processesCount)   # CREATE POOL
    height = originalImage.shape[0] # GET THE HEIGHT OF THE IMAGE
    ranges = [] # CREATE AN EMPTY ARRAY TO FILL WITH ROW SLICES FOR EACH PROCESSOR

    for i in range(processesCount): # CREATE AND APPEND RANGES
        steps = i*int(height/processesCount)
        myRange = range(steps,steps+int(height/processesCount)+1) 
        ranges.append(myRange)

    slices = p.map(SWT_apply_parallel,ranges) # CALL THE PROCESSORS 
    
    SWTMap = np.concatenate(slices, axis=0) 

    component_map , components  = CC(SWTMap)

    return SWTMap, component_map, components

