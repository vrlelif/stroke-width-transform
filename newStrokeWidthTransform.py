import numpy as np

def SWT_apply_new(edgeImage, SW_Map, gradientDirections , direction = 1):

    edgePointRows, edgePointCols =  np.nonzero(edgeImage) 
    rays = [] 
    for index in range(len(edgePointRows)):
        i = edgePointCols[index]
        j = edgePointRows[index]

        startGradient = gradientDirections[j, i]  

        startX = np.cos(startGradient)
        startY = np.sin(startGradient)    

        steps = 1 

        ray = [(j, i)]
        
        while  steps < 500: # TODO:  FIND A VALUE TO LIMIT STROKE WIDTH
            x_q = np.int32(round(i + (direction * startX * steps)))
            y_q = np.int32(round(j + (direction * startY * steps)))

            steps = steps + 1

            if not (0 <= x_q < edgeImage.shape[1] and 0 <= y_q < edgeImage.shape[0]):
                break
            
            ray.append((y_q, x_q))

            if edgeImage[y_q, x_q] > 0:
    
                strokeW = np.sqrt( (x_q - i) ** 2 + (y_q - j) ** 2)

                theta = np.abs(np.abs(startGradient - gradientDirections[y_q, x_q]) - np.pi)

                if theta <= np.pi / 2:
                    for ry, rx in ray:
                        SW_Map[ry, rx] = min(SW_Map[ry, rx], strokeW)
                    rays.append(ray) 
                break
            

    for ray in rays: 
        counter = 0

        median = np.median([SW_Map[y, x] for (y, x) in ray])

        for (y, x) in ray:
            try:
                #SW_Map[y, x] = min(median, SW_Map[y, x])
                leftN = SW_Map[y,x-1]
                aboveN = SW_Map[y-1,x]
                bottomN = SW_Map[y+1,x] 
                rightN = SW_Map[y,x+1]

                if len([i for i in [leftN,aboveN,bottomN,rightN] if i== float("inf")]) >= 2:
                    counter = counter + 1

            except IndexError:
                continue

        if counter < len(ray)/2:
            for (y, x) in ray:
                SW_Map[y, x] = min(median, SW_Map[y, x])
                #pass
        else:
            for (y, x) in ray:
                SW_Map[y, x] = float("inf")

                
    return SW_Map



    '''
    processesCount = 5 # DECLARE NUMBER OF PROCESSORS
    p = Pool(processes = processesCount)   # CREATE POOL
    height = originalImage.shape[0] # GET THE HEIGHT OF THE IMAGE
    ranges = [] # CREATE AN EMPTY ARRAY TO FILL WITH ROW SLICES FOR EACH PROCESSOR

    for i in range(processesCount): # CREATE AND APPEND RANGES
        steps = i*int(height/processesCount)
        myRange = range(steps,steps+int(height/processesCount)+1) 
        ranges.append(myRange)

    slices = p.map(SWT_apply_parallel,ranges) # CALL THE PROCESSORS 

    #SWTMap = np.sum(slices, axis=0) 

    asfd = np.zeros(edgeImage.shape)


    for s in slices:
        np.add(asfd,)

    SWTMap = np.add(0, slices.sum(axis=0))

    '''
