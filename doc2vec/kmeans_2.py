
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd 
from sklearn.cluster import KMeans



# In[4]:

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
            error_j = abs_delta_fj.sum()#クラスター内の平均誤差
            n_j = (model.labels_==j).sum()#クラスター内の要素数
            exp_error_j = error_j/n_j#クラスターの良しあしを測ってる指標：exp_error_j
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

    best_cent_title = []
    for i in range(len(best_cluster)):
        cent_and_titles_of_cluster_i = [kmeans_models[int(best_classifier)].cluster_centers_[int(best_cluster[i])].tolist(), kmeans_models[int(best_classifier)].labels_==int(best_cluster[i])]
        best_cent_title.append(cent_and_titles_of_cluster_i)
    return best_cent_title




# In[35]:
#get_c_and_t()...centroid and title
#classify を所定のデータ形式に対して使えるようにしたもの

def get_c_and_t(data):
    features = []
    titles = []
    for i in range(len(data)):
        features.append(data[i][1])
        titles.append(data[i][0])
    cent_and_title = classify(pd.DataFrame(features))
    for i in range(len(cent_and_title)):
        cent_and_title[i][1] = pd.DataFrame(titles)[cent_and_title[i][1]].T.as_matrix().tolist()[0]
    return cent_and_title


# In[17]:
#貰ったデータの再整形

import re

data0 = pd.read_csv("ryuya's_picked_articles")
data0.head()


# In[28]:

#文字列をリストに起こす
def enlist(str_list):
    divided_list = re.findall("[-0-9.]+",str(str_list))
    float_list = []
    for i in range(len(divided_list)):
        float_list.append(float(divided_list[i]))
    return float_list

list0 = np.array(enlist(data0.vectorized_title[0]))
list0 + np.random.standard_normal(300)
list1 = []
for i in range(50):
    list1.append( [i,(list0 + np.random.standard_normal(300)).tolist()])


# In[36]:
#get_c_and_t()　の挙動確認

get_c_and_t(list1)


# In[40]:
#classify()の挙動チェック
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

classify(features)
