import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

epsilon = 2
def euclideanDistance(row1, row2):
    distance = 0
    for i in range(len(row1)):
        distance += np.power((row2[i] - row1[i]), (2))
    distance = np.sqrt(distance)
    return distance

d = {'c1': [1, 0, 1, 10, 11, 10],'c2': [1, 0, 0, 10,  10, 11]}


df = pd.DataFrame(data=d)
print(df)
print(df.index)

dex = []
for i in range(0,len(df.index)):
    dex.append(i)

print(dex)

print(squareform(pdist(df.loc[dex])))

m = pd.DataFrame(squareform(pdist(df.loc[dex])),columns=df.index,index =df.index)
print(m)

lessThanEpsilonDict = {} 

for i, mRow in m.iterrows():
    if m.loc[i][0] < epsilon:
        if str(mRow) in lessThanEpsilonDict.keys():
            oldValueArray = lessThanEpsilonDict[str(mRow)]
            oldValueArray.append[i]
            lessThanEpsilonDict[str(mRow)] = oldValueArray
        else:
            lessThanEpsilonDict[str(mRow)] = [i]