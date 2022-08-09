import numpy as np  # numpy library to be able to play with arrays

def getDivision(x,y):
    try:
        if(x/y <=3) or (y/x<=3):
            return True
        else:
            return False
    except Exception as e: print(e)


def CC(SWT, direction = 1 ):
    label = 0  
    component_map =  np.zeros(SWT.shape)
    components = {}
    eq_list = {}

    [strokePointsRow,strokePointsCol] =  np.where(SWT) #get the stroke existing points

    for index,y in enumerate(strokePointsRow):
        x = strokePointsCol[index]
        # do something with the pixel at position (x, y)
        try:
            strokeOfPixel = SWT[y,x] * direction

            leftN = component_map[y,x-1]
            aboveN = component_map[y-1,x]
            topLeft = component_map[y-1,x-1] 
            topRight = component_map[y-1,x+1]

            nolabeledNeighbours = leftN == 0 and aboveN == 0 and topLeft == 0 and topRight == 0
            
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
                        
                    for n in nLabels:
                        if eq_list[n] > int(min(nLabels)):
                            eq_list[n] = int(eq_list[min(nLabels)])

                    component_map[y,x] = int(eq_list[min(nLabels)])

                    components[int(eq_list[min(nLabels)])].append([y,x])

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
                ''''
                left = component_map[y,x-1]
                above = component_map[y-1,x]
                right = component_map[y,x+1]
                bottom = component_map[y+1,x]
                topLeft = component_map[y-1,x-1]
                topRight = component_map[y-1,x+1]
                bottomRight = component_map[y+1,x+1]
                bottomLeft = component_map[y+1,x-1]
                neighbourLabels = [x for x in [left,right,above,bottom,topLeft,topRight,bottomLeft,bottomRight] if x != 0]
                '''
                val = component_map[y,x]
                if component_map[y,x] > eq_list[val]:
                    component_map[y,x] = eq_list[val]

                components[int(eq_list[val])].append([y,x])
            
        except IndexError:
            continue
        
    return component_map, eq_list, components