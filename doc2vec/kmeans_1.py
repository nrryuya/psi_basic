
# coding: utf-8

# In[2]:

import numpy as np
import pandas as pd 
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.cluster import KMeans

# 生徒の国語・数学・英語の各得点を配列として与える
features = pd.DataFrame([[ 80,  96,  54,  80,  90,  84,  79,  88,  98,  75,  92,  96,  99,
         75,  90,  54,  92,  88,  42,  70,  94,  52,  94,  70,  95,  95,
         75,  49,  83,  75,  79, 100,  88, 100,  55,  92,  97],
       [ 85, 100,  83,  98,  92,  78, 100,  92,  73,  84, 100,  92,  76,
         82,  94,  84,  89,  94,  99,  98,  78,  73,  88,  73,  84,  88,
         97,  81,  72,  73,  82,  77,  63,  50,  96,  74,  50],
       [100, 100,  98,  98,  91,  82,  96,  92,  72,  85,  96,  90,  91,
         88,  94,  87,  62,  97,  80,  70,  83,  87,  72,  80,  90,  84,
         89,  86,  80,  88,  76,  89,  79,  86,  84,  77,  73]]).T
features.columns = ["Japanese","Math","English"]


# In[13]:

# K-means クラスタリングをおこなう
# この例では 3 つのグループに分割 (メルセンヌツイスターの乱数の種を 10 とする)
def classify(features):
    kmeans_models =[KMeans(n_clusters=i, random_state=10).fit(features)  for i in range(1,21)]
    # 分類先となったラベルを取得する
    labels = [ kmeans_models[0].labels_ for i in range(20)]
    
    n = 20#20
    distortions = []
    densities = []

    for i in range(1,n):
        model = kmeans_models[i]
        distortions.append(model.inertia_)
    
        for j in range(i):
            #誤差の絶対値の平均を求める
            fj = features[model.labels_==j]
            abs_delta_fj = np.sqrt( ((fj - fj.mean())**2).mean() )
            error_j = abs_delta_fj.sum()
            exp_error_j = error_j/(model.labels_==j).sum()
            densities.append([i,j,exp_error_j])
    densities = np.array(densities)
    densities[densities.T[2]==0] = 100

    densities
    sup = np.sort(densities.T[2])[20]


    pd_densities = pd.DataFrame(densities)
    pd_densities["good_cluster"] = densities.T[2]<=sup
    pd_densities.columns = ["#cluster","index_of_cluster","density","good_cluster"]
    best_classifier =  pd_densities.groupby(by = "#cluster")["good_cluster"].sum().argmax()
    best_classifier
    print(type(best_classifier))

    best_densities = pd_densities[pd_densities["#cluster"]==best_classifier]
    best_cluster = best_densities["index_of_cluster"][best_densities["good_cluster"]==True]
    best_cluster.index = range(len(best_cluster))
    best_cluster

    best_centroids = []
    for i in range(len(best_cluster)):
        best_centroids.append(kmeans_models[int(best_classifier)].cluster_centers_[int(best_cluster[i])].tolist())
        best_centroids.append(kmeans_models[int(best_classifier)].labels_==int(best_cluster[i]))
    return best_centroids
classify(features)


# fj = model4_3
# abs_delta_fj = np.abs( fj - fj.mean() )
# error_j = abs_delta_fj.sum()
