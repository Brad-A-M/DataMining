# -*- coding: utf-8 -*-
"""
@author: dkelly

1: centroids are randomly selected from dataSet in initCentroids()
2: point is selected from dataSet and assigned to  cluster in assignNewPointToCluster()
    a: euclideanDistance() is called to assign to closest existing cluster
3: centroid of the cluster the point was assigned to is recalculated in recalculateCentroids()
4: all assigned points are compared against new centroids to assign new cluster in reassignClusters()
5: repeat 2-4 for all points in data set
"""
import numpy as np
import pandas as pd
import sys
import math

class Kmeans:

    def __init__(self, k, dataSet, isClassification):
        self.k = k
        self.original_dataset = dataSet
        self.isClassification = isClassification
        # temporarily drop class column if it is a classification dataset
        if isClassification:
            self.dataSet = dataSet.drop(dataSet.columns[-1], axis = 1)
        else:
            self.dataSet = dataSet
        self.dataSet["cluster"] = -1
        self.centroids = pd.DataFrame(columns=self.dataSet.columns)
        self.initCentroids(self.k, self.dataSet)
        self.generateClusters(self.k) # pass self.dataSet since rows were dropped from local data set
        self.updateCentroids()
    
    def initCentroids(self, k, dataSet):
        #dataSet is temporary copy of self.dataSet
        #all points are preserved in self.dataSet because even points selected for centroids cannot be removed
        for i in range(k): # init k centroids
            row = np.random.randint(0, dataSet.shape[0]) # random number between zero and row count
            self.centroids = self.centroids.append(dataSet.iloc[row,:])
            self.centroids.reset_index(inplace=True, drop=True)
            self.centroids.loc[self.centroids.index[i],"cluster"] = i #assign each centroid to its corresponding cluster
            dataSet = dataSet.drop(dataSet.index[row])
            dataSet.reset_index(inplace=True, drop=True)
    
    def generateClusters(self, k):
        for i in range(len(self.dataSet)):   #iterate through each point in the data set
            row = self.dataSet.iloc[i, :]   #get row at index i
            distance = sys.maxsize
            for index, centroid in self.centroids.iterrows(): #compare the distance of each point to each of the centroids
                new_distance = self.euclideanDistance(row, centroid)
                if new_distance < distance :    #if new distance is shorter, put row in the new cluster
                    row["cluster"] = centroid["cluster"]
                    distance = new_distance #update the distance for next comparison
            self.dataSet.loc[self.dataSet.index[i], "cluster"] = row["cluster"] #update the cluster for the row in the data set

    def updateCentroids(self):
        dataset = self.dataSet
        centroids = self.centroids
        for cluster_name in range(len(self.centroids)): #get the name of the cluster from the centroids data frame 
            cluster = self.dataSet.loc[self.dataSet["cluster"] == cluster_name] #get all points in cluster from the data set
            if len(cluster) > 0:
                cluster.reset_index(inplace=True, drop=True) #reset index since rows grabbed might not have been sequential
                new_centroid = cluster.sum(axis=0) / len(cluster) # cluster name will hold through this despite division since all points have the same cluster name
                print("new centroid")
                print(new_centroid)
                self.centroids.loc[cluster_name] = new_centroid

    def converge(self, max_iterations):
        previous_cluster_assignment = self.dataSet["cluster"]
        # imitate do while loop
        count = 0
        while True:
            self.updateCentroids()
            print("updating clusters") #centroids need to be updated for new cluster assignments
            self.generateClusters(self.k)
            if(previous_cluster_assignment.equals(self.dataSet["cluster"]) or count == max_iterations): #check to see if assignments have changed
                break
            else:
                previous_cluster_assignment = self.dataSet["cluster"] #previous cluster assignments become current if cluster assignments were updated
                count += 1
                print(count)
        return self.centroids

    def euclideanDistance(self, row, centroid):
        distance = 0
        for i in range(len(row) - 1): # don't include cluster
            distance += np.power((centroid[i] - row[i]),(2)) 
        distance = np.sqrt(distance)
        return distance
    
    def getClusters(self, max_iterations):
        centroids = self.converge(max_iterations)
        clusters = self.dataSet
        dataset = self.original_dataset
        #re-insert class if classification
        if self.isClassification:
            clusters["class"] = dataset[dataset.columns[len(dataset.columns)-1]]
            #swap class and cluster column order
            new_col_order = list(clusters.columns.values)
            new_col_order[len(new_col_order) - 2] = "class"
            new_col_order[len(new_col_order) - 1] = "cluster"
            clusters = clusters.reindex(columns = new_col_order)
            
        return clusters