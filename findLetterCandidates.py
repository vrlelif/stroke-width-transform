import numpy as np

def getDivision(x,y):
    try: 
        return (x/y <=3) or (y/x<=3)
    except Exception: 
        pass

def CC(SWT, direction, originalImage ):
    label = 0  
    component_map =  np.zeros(SWT.shape)
    components = {}
    eq_list = {}
    [strokePointsRow,strokePointsCol] =  np.where(SWT) 
    for y in range(SWT.shape[0]):
        for x in  range(SWT.shape[1]):
            if SWT[y,x] == float("inf"):
                continue
            try:
                strokeOfPixel = SWT[y,x] * direction
                leftN = component_map[y,x-1]
                aboveN = component_map[y-1,x]
                topLeft = component_map[y-1,x-1] 
                topRight = component_map[y-1,x+1]
                nolabeledNeighbours = sum([leftN,aboveN,topLeft,topRight]) == 0
                
                nLabels = []
                if not nolabeledNeighbours :
                    if(leftN > 0 and getDivision(leftN,strokeOfPixel)):
                        nLabels.append(component_map[y,x-1])
                    if(aboveN > 0  and getDivision(aboveN,strokeOfPixel)):
                        nLabels.append(component_map[y-1,x])
                    if(topLeft > 0 and getDivision(topLeft,strokeOfPixel)):
                        nLabels.append(component_map[y-1,x-1])
                    if(topRight > 0  and getDivision(topRight,strokeOfPixel)):
                        nLabels.append(component_map[y-1,x+1])
                    if len(nLabels)>1:
                        max = int(np.max(nLabels))
                        min = int(np.min(nLabels))
                        component_map[y,x] = min
                        eq_list[max] = min
                    else:
                        component_map[y,x] = np.min(nLabels)
                elif nolabeledNeighbours:
                    
                    label += 1
                    eq_list[label] = label
                    component_map[y,x] = label
                    if hasattr(components, str(label)):
                        components[label].append([y,x])
                    else:
                        components[label] = []
                        components[label].append([y,x])
            except IndexError:
                continue
    
    [componentPointsRow,componentPointsCol] =  np.where(component_map) #get the label existing points
    for index,y in enumerate(componentPointsRow):
        x = componentPointsCol[index]
        try:
            currentLabel = component_map[y,x]
            newLabel = eq_list[currentLabel]
            component_map[y,x] = newLabel
            
            components[newLabel].append([y,x])
            
        except IndexError:
            continue
    components = {k: v for k, v in components.items() if len(v) > 1}
    
    return component_map,components

def findLetterCandidates(component_map, components , SWTResult, originalImage):
    newResult  =  np.zeros(component_map.shape)
    features = {}
    for component in list(components):
        c = np.unique(components[component], axis=0)
        arrS = [SWTResult[p[0], p[1]] for p in c]
        height = max(c[:,0]) - min(c[:,0]) + 1
        width =  max(c[:,1]) - min(c[:,1]) + 1
        aspect = width  / height
        varianceV = np.var(arrS)
        averageV = np.mean(arrS)
                
        median = np.median(arrS)
        diameter = np.sqrt( height ** 2 + width ** 2)
        componentArea = component_map[ min(c[:,0]): min(c[:,0]) + height, min(c[:,1]):min(c[:,1] ) + width]

        uniqueArr = np.unique(componentArea)
        '''CONDITIONS'''
        varianceRatio = (varianceV/averageV) < 2 
        aspectRatio = 0.1 <= aspect < 10
        diameterRatio = (median / diameter) < 15.00
        heightV = 10 < height < 300
        widthV =  10 < width < 300
        compCount = len(uniqueArr[uniqueArr != 0]) <= 3
        '''

        
        if not varianceRatio :
            continue
        if not  aspectRatio :
            continue
        if not  diameterRatio :
            continue

        if not  compCount: 
            continue
        
        
        if not  heightV :
            continue
        if not  widthV :
            continue

        '''

        for p in components[component]:
            newResult[p[0],p[1]] = component
    
        originalImageSliceNoNZero = originalImage[ min(c[:,0]): min(c[:,0]) + height, min(c[:,1]):min(c[:,1] ) + width]
        componentMapSlice = newResult[ min(c[:,0]): min(c[:,0]) + height, min(c[:,1]):min(c[:,1] ) + width]
        #avg_color_per_row_BEFORE = np.average(originalImageSliceNoNZero,axis=0)
        originalImageSliceNoNZero = originalImageSliceNoNZero[componentMapSlice > 0 ]
        avg_color = np.average(originalImageSliceNoNZero,axis=0)
        features[component] = {
            'medianS' : median,
            'height' : height,
            'width' : width,
            'maxX' :  max(c[:,1]),
            'minX' : min(c[:,1]),
            'maxY' :  max(c[:,0]),
            'minY' : min(c[:,0]),
            'avgColor' : avg_color,
            'locations' : c
        }
                
    return newResult, features
