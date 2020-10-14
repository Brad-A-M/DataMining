# -*- coding: utf-8 -*-
import load_dataset as ld
import kmeans as km
import numpy as np
import math
import pandas as pd

class Main:
        def __init__(self):
                #define variable to use inside class which may need tuning      
                self.alldataset = ld.LoadDataset().load_data()          #load all datasets
                #check dataset is classification
                self.IsClassificationDict = ld.LoadDataset().IsClassificationDict()
                
        def main(self):
                for dataset in self.alldataset:         #for each dataset call each algorithm
                        print('current dataset ::: {0} \n'.format(dataset))
                        data = self.alldataset.get(dataset)
                        isClassification = self.IsClassificationDict.get(dataset)
                        k = 5
                        kmeans = km.Kmeans(k, data, isClassification)
                        clusters = kmeans.getClusters(3) #max of 3 iterations
                        print('Finished with kmeans')
                return clusters
                                  
results = Main().main()
print('Finished')