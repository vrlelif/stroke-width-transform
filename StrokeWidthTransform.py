import numpy as np

def SWT_apply(edgeImage, SW_Map, gradientDirections , direction = 1):

    edgePointRows, edgePointCols =  np.nonzero(edgeImage) 
  
    rays = [] 

    for index,j in enumerate(edgePointRows):
        
        i = edgePointCols[index]

        startGradient = gradientDirections[j, i]  

        startX = np.cos(startGradient)
        startY = np.sin(startGradient)

        steps = 1

        ray = [(j, i)]
        
        while  True: # TODO:  FIND A VALUE TO LIMIT STROKE WIDTH
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
        median = np.median([SW_Map[y, x] for (y, x) in ray])
        for (y, x) in ray:
            SW_Map[y, x] = min(median, SW_Map[y, x]) 

    SW_Map[SW_Map == np.Infinity] = 0
 

    return SW_Map
