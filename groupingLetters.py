import numpy as np

def findDistance(co1,co2):
    widerCompWidth = min(co1['width'],co2['width'])
    if co1['minY'] >= co2['maxY'] or co2['minY'] >= co1['maxY']:
        return False
    else:
        dist = np.sqrt((co2['maxY'] - co1['maxY']) ** 2 + (co2['minX'] - co1['maxX']) ** 2)
        return dist <= widerCompWidth * 3

def findPairs(components):
    pairs = []
    for co in components:
        for can in components:
            if co == can:
                continue
            strokeM = components[co]['medianS'] / components[can]['medianS']  <= 2
            heights = components[co]['height'] / components[can]['height']  <= 2
            distance =  findDistance(components[co],components[can])
            colors = np.mean(components[co]['avgColor']) / np.mean(components[can]['avgColor']) <= 3
            if (strokeM and heights and distance and colors):
                pairs.append([co,can])
    return pairs

def groupG(pairs):
    groups = []
    if len(pairs) > 1:
        for i,pair in enumerate(pairs):
            try:
                if (any(point in pairs[i+1] for point in pair)):
                    group = np.concatenate(( pair,pairs[i+1]))
                    group = np.unique(group)
                    groups.append(group)
            except IndexError:
                continue
            
    if len(groups) == 0 :
        groupsFiltered = np.array([row for row in pairs if len(row)>=3])
        return groupsFiltered
    else: 
        return groupG(groups)
