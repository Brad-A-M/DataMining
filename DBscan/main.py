import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

epsilon = 2
minPts = 2
d = {'c1': [1, 0, 1, 10, 11, 10],'c2': [1, 0, 0, 10,  10, 11]}

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


df, dex = init()
m = createPairwiseDistanceMatrix(df)
lessThanEpsilonDict = createLessThanEpsilonDict(df, m)

print(lessThanEpsilonDict)