import numpy as np

def getDivision(x,y):
    try: 
        return (x/y <=3) or (y/x<=3)
    except Exception: 
        pass

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
