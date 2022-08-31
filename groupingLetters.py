from math import sqrt
from statistics import mean
import networkx as nx

def findDistance(co1,co2):
    widerCompWidth = min(co1['width'],co2['width'])
    if co1['minY'] >= co2['maxY'] or co2['minY'] >= co1['maxY']:
        return False
    else:
        dist = sqrt((co2['maxY'] - co1['maxY']) ** 2 + (co2['minX'] - co1['maxX']) ** 2)
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
            colors = mean(components[co]['avgColor']) / mean(components[can]['avgColor']) <= 3
            if (strokeM and heights and distance and colors):
                pairs.append((co,can))
    return pairs

def findPairsAlternative(components):
    L = list(components.keys())

    edges = [(x,y) for x in L for y in L if 
    components[x]['medianS'] / components[y]['medianS']  <= 2 and 
    components[x]['height'] / components[y]['height']  <= 2 and 
    findDistance(components[x],components[y]) and 
    mean(components[x]['avgColor']) / mean(components[y]['avgColor']) <= 3 and 
    x!=y]
    return edges

def groupG(pairs):
    edges = pairs
    graph = nx.Graph(edges) 
    return [tuple(c) for c in nx.connected_components(graph)]

def groupingLettersIntoTextLines(components):
    pairs = findPairsAlternative(components)
    return groupG(pairs)

    
