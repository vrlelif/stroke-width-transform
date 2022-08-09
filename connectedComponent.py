import numpy as np

def getDivision(x,y):
    try:
        if(x/y <=3) or (y/x<=3):
            return True
        else:
            return False
    except Exception as e: 
        print(e)


def CC(SWT, direction = 1 ):
    label = 0  
    component_map =  np.zeros(SWT.shape)
    components = {}
    eq_list = {}

    [strokePointsRow,strokePointsCol] =  np.where(SWT) 

    for index,y in enumerate(strokePointsRow):
        x = strokePointsCol[index]
        try:
            strokeOfPixel = SWT[y,x] * direction

            leftN = component_map[y,x-1]
            aboveN = component_map[y-1,x]
            topLeft = component_map[y-1,x-1] 
            topRight = component_map[y-1,x+1]

            nolabeledNeighbours = sum([leftN,aboveN,topLeft,topRight]) == 0
            
            nLabels = []

            if strokeOfPixel > 0:
                if not nolabeledNeighbours :
                    if(leftN > 0 and getDivision(leftN,strokeOfPixel)):
                        nLabels.append(component_map[y,x-1])
                    if(aboveN > 0  and getDivision(aboveN,strokeOfPixel)):
                        nLabels.append(component_map[y-1,x])
                    if(topLeft > 0 and getDivision(topLeft,strokeOfPixel)):
                        nLabels.append(component_map[y-1,x-1])
                    if(topRight > 0  and getDivision(topRight,strokeOfPixel)):
                        nLabels.append(component_map[y-1,x+1])

                    ref = eq_list[min(nLabels)]
                        
                    for n in nLabels:
                        if eq_list[n] > min(nLabels):
                            eq_list[n] = ref

                    component_map[y,x] = ref

                    components[ref].append([y,x])

                elif nolabeledNeighbours:
                    
                    label += 1
                    eq_list[label] = label
                    component_map[y,x] = label

                    if hasattr(components, str(label)):
                        components[label].append([y,x])
                    else:
                        components[label] = []
                        components[label].append([y,x])
            else:
                component_map[y,x] = 0
        
        except IndexError:
            continue
    
    [componentPointsRow,componentPointsCol] =  np.where(component_map) #get the label existing points

    for index,y in enumerate(componentPointsRow):
        x = componentPointsCol[index]

        try:
            if component_map[y,x] > 0:
                val = component_map[y,x]
                if component_map[y,x] > eq_list[val]:
                    component_map[y,x] = eq_list[val]

                components[eq_list[val]].append([y,x])
            
        except IndexError:
            continue

    newResult  =  np.zeros(component_map.shape)

    for component in list(components):
        '''calculate variance rate'''
        arrS = [SWT[p[0], p[1]] for p in components[component]]
        
        arrY = sorted(components[component], key=lambda x: x[0])
        arrX = sorted(components[component], key=lambda x: x[1])

        minY  =  arrY[0][0]
        maxY  =  arrY[len(arrY) - 1 ][0]
        minX  =  arrX[0][1]
        maxX  =  arrX[len(arrX) - 1 ][1]

        height = maxY - minY + 1
        width = maxX - minX + 1

        aspect = width  / height

        varianceV = np.var(arrS)
        averageV = np.mean(arrS)
        
        median = np.median(arrS)
        diameter = np.sqrt( height ** 2 + width ** 2)
        uniqueArr = np.unique(component_map[minY:maxY, minX:maxX])

        '''CONDITIONS'''
        varianceRatio = (varianceV/averageV) <= 2 
        aspectRatio = 0.1 <= aspect <= 10
        diameterRatio = (median / diameter) <= 15.00
        heightV = 10 <= height <= 300
        widthV =  10 <= width <= 300
        compCount = len(uniqueArr[uniqueArr != 0]) <=3

        if varianceRatio and aspectRatio and diameterRatio and heightV and widthV and compCount:
            #result = cv2.rectangle(result, (minX,minY ), (minX + width ,minY+height), (255,0,255), 1)
            for p in components[eq_list[component]]:

                newResult[p[0],p[1]] = eq_list[component]
                
    return newResult, eq_list, components 