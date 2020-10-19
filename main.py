# -*- coding: utf-8 -*-
import load_dataset as ld
import kmeans as km
import numpy as np
import math
import pandas as pd
import synthetic_data as sd
import db_scan as db
import assessment

class Main:
        def __init__(self):
                #define variable to use inside class which may need tuning      
                self.alldataset = ld.LoadDataset().load_data()          #load all datasets
                #check dataset is classification
                self.IsClassificationDict = ld.LoadDataset().IsClassificationDict()
                
        def main(self):
                
                # create synthetic dataset
                synthesizer = sd.SyntheticData(5,5,10,6)
                pts = synthesizer.point_assignments # synthetic data pts
                # TODO: might attempt to plot clusters if time permits.
                #print(pts.head(30))


                
                # k-means setup for synthetic dataset
                print('Running k-means with synthetic dataset...')
                kmeans = km.Kmeans(5, pts, False, True)
                kmeans_clusters = kmeans.getClusters(3) # max of 3 iterations
                print('Finished k-means with synthetic dataset')
                print('Calculating average silhouette coefficient...')
                kmeans_silhouette = assessment.calculate_silhouette(kmeans_clusters)
                print('Average k-means silhouette coefficient = {0}\n'.format(kmeans_silhouette))
                
                # DB Scan setup for synthetic dataset
                print('Running DB Scan with synthetic dataset...')
                epsilon = 2
                minPts = 2
                dbScan = db.DbScan(pts, False, True)
                df, dex = dbScan.getDataframe()
                m = dbScan.createPairwiseDistanceMatrix(df, dex)
                lessThanEpsilonDict = dbScan.createLessThanEpsilonDict(df, m, epsilon)
                dbScan_clusters = dbScan.clusterAssignment(df, lessThanEpsilonDict, minPts)
                print('Finished DB Scan with synthetic dataset')
                print('Calculating average silhouette coefficient...')
                dbScan_silhouette = assessment.calculate_silhouette(dbScan_clusters)
                print('Average DB Scan silhouette coefficient = {0}\n'.format(dbScan_silhouette))

                # k-means and DB scan for classification datasets from UCI repository
                for dataset in self.alldataset:         # for each dataset call each algorithm
                        print('current dataset ::: {0} \n'.format(dataset))
                        data = self.alldataset.get(dataset)
                        isClassification = self.IsClassificationDict.get(dataset)
                        
                        print('Running k-means on dataset ::: {0}... \n'.format(dataset))
                        k = 5
                        kmeans = km.Kmeans(k, data, isClassification, False)
                        kmeans_clusters = kmeans.getClusters(3) #max of 3 iterations
                        print('Finished kmeans for {0} dataset\n'.format(dataset))
                        print('Calculating purity...')
                        kmeans_purity = assessment.calculate_purity(kmeans_clusters)
                        print('k-means purity on dataset ::: {0} = {1} \n'.format(dataset, kmeans_purity))
                        
                        print('Running DB Scan on dataset ::: {0}... \n'.format(dataset))
                        epsilon = 2
                        minPts = 2
                        dbScan = db.DbScan(data, isClassification, False)
                        df, dex = dbScan.getDataframe()
                        m = dbScan.createPairwiseDistanceMatrix(df, dex)
                        lessThanEpsilonDict = dbScan.createLessThanEpsilonDict(df, m, epsilon)
                        dbScan_clusters = dbScan.clusterAssignment(df, lessThanEpsilonDict, minPts)
                        print('Finished DB Scan for {0} dataset\n'.format(dataset))
                        print('Calculating purity...')
                        dbScan_purity = assessment.calculate_purity(dbScan_clusters)
                        print('DB Scan purity on dataset ::: {0} = {1} \n'.format(dataset, dbScan_purity))
                                  
Main().main()
print('Finished')