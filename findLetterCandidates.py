import numpy as np

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
        varianceRatio = (varianceV/averageV) <= 2 
        aspectRatio = 0.1 <= aspect <= 10
        diameterRatio = (median / diameter) <= 15.00
        heightV = 10 <= height <= 300
        widthV =  10 <= width <= 300
        compCount = len(uniqueArr[uniqueArr != 0]) <=3
        if not varianceRatio :
            continue
        if not  aspectRatio :
            continue
        if not  diameterRatio :
            continue
        if not  heightV :
            continue
        if not  widthV :
            continue
        if not  compCount: 
            continue

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
            'avgColor' : avg_color
        }
                
    return newResult, features
