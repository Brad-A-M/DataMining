import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

# global variables
epsilon = 2
minPts = 2
d = {'c1': [1, 0, 1, 10, 11, 10, 90],'c2': [1, 0, 0, 10,  10, 11, 50]}

# initalize dataframe
def init():
    df = pd.DataFrame(data=d)
    dex = []
    for i in range(0,len(df.index)):
        dex.append(i)
    return df, dex

def createPairwiseDistanceMatrix(df):
    m = pd.DataFrame(squareform(pdist(df.loc[dex])),columns=df.index,index =df.index)
    return m

def createLessThanEpsilonDict(df, m):
    lessThanEpsilonDict = {}
    for i in range(len(df)):
        for j in range(len(df)):
            if m.loc[i,j]< epsilon:
                if i in lessThanEpsilonDict.keys():
                    oldValueArray = []
                    oldValueArray = lessThanEpsilonDict[i]
                    oldValueArray.append(j)
                    lessThanEpsilonDict[i] = oldValueArray
                else:
                    arrayToAppend = []
                    arrayToAppend.append(j)
                    lessThanEpsilonDict[i] = arrayToAppend
    return lessThanEpsilonDict

def clusterAssignment(cf, lessThanEpsilonDict):
    clusters = []
    # cluster -2 means unassigned, -1 means noise
    c = 0;
    for i in range(0, len(df.index)):
        clusters.append(-2)

    for point in range(0, len(df.index)):
        if clusters[point] != -2:
            continue
        if clusters[point] == -2:
            if len(lessThanEpsilonDict[point]) < minPts:
                clusters[point] = -1
            else:
                c = c + 1
                clusters[point] = c

                stack = []
                for nearNeighbor in lessThanEpsilonDict[point]:
                    if(point!=nearNeighbor):
                        stack.append(nearNeighbor)

                while (len(stack) != 0):
                    q = stack.pop()

                    if clusters[q] == -1:
                        clusters[q] = c
                    if clusters[q] != -2:
                        continue
                    else:
                        clusters[q] = c
                        if len(lessThanEpsilonDict[q]) >= minPts:
                            for nearNeighbor in lessThanEpsilonDict[q]:
                                if(nearNeighbor != q):
                                    stack.append(nearNeighbor)

    print(clusters)


df, dex = init()
m = createPairwiseDistanceMatrix(df)
lessThanEpsilonDict = createLessThanEpsilonDict(df, m)
clusterAssignment(df, lessThanEpsilonDict)


