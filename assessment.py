import pandas as pd
### SILHOUETTE
def calculate_silhouette(df):
    point_df = df.drop(columns = ['cluster'])
    df['intra_distance'] = np.zeros(len(df))
    df['inter_distance'] = np.zeros(len(df))
    df['silhouette_coeff'] = np.zeros(len(df))
    index = 0
    for point in point_df.to_numpy():
        cluster_dist_dict = {}
        intra_total = 0
        inter_total = float('INF')
        intra_points = 0
        reference_cluster = df['cluster'].iloc[index]

        distance_df = (point_df - point)**2
        distances = (distance_df.sum(axis=1))**0.5

        for i in range(len(distances)):
            if df['cluster'].iloc[i] == reference_cluster:
                intra_total += distances[i]
                intra_points += 1

            else:
                if df['cluster'].iloc[i] not in cluster_dist_dict.keys():
                    cluster_dist_dict[df['cluster'].iloc[i]] = [distances[i]]
                else:
                    cluster_dist_dict[df['cluster'].iloc[i]].append(distances[i])
        print('cluster dict \n', cluster_dist_dict)
        for key in cluster_dist_dict.keys():
            if sum(cluster_dist_dict[key]) < inter_total:
                inter_total = sum(cluster_dist_dict[key])
                inter_points = len(cluster_dist_dict[key])
        print("point", point, 'dist', inter_total, 'num pts', inter_points)


        intra_dist = intra_total/(intra_points-1)
        inter_dist = inter_total/inter_points
        df['intra_distance'].iloc[index] = intra_dist
        df['inter_distance'].iloc[index] = inter_dist
        df['silhouette_coeff'].iloc[index] = (inter_dist - intra_dist)/max(intra_total, inter_dist)
        index+=1

    return df['silhouette_coeff'].mean()
    







### PURITY OR CONDITIONAL ENTROPY
def calculate_purity(df):
    total_intersections = 0
    for c in df['class'].unique():
        class_mask = df['class'].mask(df['class']==c, 1).mask(df['class']!=c, 0)
        intersections = []
        for l in df['cluster'].unique():
            cluster_mask = df['cluster'].mask(df['cluster']==l, 1).mask(df['cluster']!=l, 0)
            sum_mask = class_mask + cluster_mask
            sum_mask = sum_mask.mask(sum_mask == 2, 1).mask(sum_mask != 2, 0)
            intersections.append(sum_mask.sum())
        total_intersections += max(intersections)
    # print(total_intersections)
    purity = total_intersections/len(df)
    # print(purity)
    return purity

