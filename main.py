# -*- coding: utf-8 -*-
import load_dataset as ld
import kmeans as km
import numpy as np
import math
import pandas as pd
import synthetic_data as sd

class Main:
        def __init__(self):
                #define variable to use inside class which may need tuning      
                self.alldataset = ld.LoadDataset().load_data()          #load all datasets
                #check dataset is classification
                self.IsClassificationDict = ld.LoadDataset().IsClassificationDict()
                
        def main(self):
                synthesizer = sd.SyntheticData(5,5,10,6)
                pts = synthesizer.point_assignments # synthetic data pts
                # TODO: might attempt to plot clusters if time permits.
                print(pts.head(30))
                synthetic_km = km.Kmeans(5, pts, False)
                clusters = synthetic_km.getClusters(3) #max of 3 iterations
                print('Finished kmeans with synthetic dataset')

                for dataset in self.alldataset:         #for each dataset call each algorithm
                        print('current dataset ::: {0} \n'.format(dataset))
                        data = self.alldataset.get(dataset)
                        isClassification = self.IsClassificationDict.get(dataset)
                        k = 5
                        kmeans = km.Kmeans(k, data, isClassification)
                        clusters = kmeans.getClusters(3) #max of 3 iterations
                        print('Finished kmeans for {0} dataset\n'.format(dataset))
                
                                  
Main().main()
print('Finished')