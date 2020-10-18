import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

class DbScan:

    # initalize dataframe
    def __init__(self, df, isClassification, isSynthetic):
        self.dex = []
        for i in range(0,len(df.index)):
            self.dex.append(i)

        self.original_df = df
        # temporarily drop class column if it is a classification dataset
        # use index rather than column name because not all datasets refer to the
        # classes as 'class', but all have the classes in the last column
        if isClassification:
            self.original_df = df.rename(columns={"CLASS": "class"})
            self.df = df.drop(df.columns[-1], axis = 1)
        # temporarily drop polygon column if it is a synthetic dataset
        elif isSynthetic:
            self.df = df.drop(columns=["polygon"])

    def getDataframe(self):
        return self.df, self.dex

    def createPairwiseDistanceMatrix(self, df, dex):
        m = pd.DataFrame(squareform(pdist(df.loc[dex])),columns=df.index,index =df.index)
        return m

    def createLessThanEpsilonDict(self, df, m, epsilon):
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

    def clusterAssignment(self, df, lessThanEpsilonDict, minPts):
        clusters = []
        # cluster -2 means unassigned, -1 means noise
        c = 0
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
            cluster_df = self.original_df
            cluster_df["cluster"] = clusters
        return cluster_df
