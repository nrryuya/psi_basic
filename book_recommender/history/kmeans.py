# coding: utf-8
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


# K-means クラスタリングをおこなう
# この例では 3 つのグループに分割 (メルセンヌツイスターの乱数の種を 10 とする)
def classify(features):
    kmeans_models = [KMeans(n_clusters=i, random_state=10).fit(features) for i in range(1, 21)]
    # 分類先となったラベルを取得する
    labels = [kmeans_models[0].labels_ for i in range(20)]

    n = 20  # 20
    distortions = []
    densities = []

    for i in range(1, n):
        model = kmeans_models[i]
        distortions.append(model.inertia_)

        for j in range(i):
            # 誤差の絶対値の平均を求める
            fj = features[model.labels_ == j]
            abs_delta_fj = np.sqrt(((fj - fj.mean())**2).mean())
            error_j = abs_delta_fj.sum()
            exp_error_j = error_j / (model.labels_ == j).sum()
            densities.append([i, j, exp_error_j])
    densities = np.array(densities)
    densities[densities.T[2] == 0] = 100

    densities
    sup = np.sort(densities.T[2])[20]

    pd_densities = pd.DataFrame(densities)
    pd_densities["good_cluster"] = densities.T[2] <= sup
    pd_densities.columns = ["#cluster", "index_of_cluster", "density", "good_cluster"]
    best_classifier = pd_densities.groupby(by="#cluster")["good_cluster"].sum().argmax()
    best_classifier
    print(type(best_classifier))

    best_densities = pd_densities[pd_densities["#cluster"] == best_classifier]
    best_cluster = best_densities["index_of_cluster"][best_densities["good_cluster"] == True]
    best_cluster.index = range(len(best_cluster))
    best_cluster

    best_cent_title = []
    for i in range(len(best_cluster)):
        cent_and_titles_of_cluster_i = [kmeans_models[int(best_classifier)].cluster_centers_[int(
            best_cluster[i])].tolist(), kmeans_models[int(best_classifier)].labels_ == int(best_cluster[i])]
        best_cent_title.append(cent_and_titles_of_cluster_i)
    return best_cent_title


# get_c_and_t()...centroid and title
# classify を[title, vector]のリストに対して使えるようにしたもの
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


# classify をtitles_dfに対して使えるようにした
def get_cluster(titles_df):
    features = []
    titles = []
    for k, v in titles_df.iterrows():
        normalized_vector = normalize(v['vectorized_title'])
        features.append(normalized_vector)
        titles.append(v['title'])
    cent_and_title = classify(pd.DataFrame(features))
    for i in range(len(cent_and_title)):
        cent_and_title[i][1] = pd.DataFrame(titles)[cent_and_title[i][1]].T.as_matrix().tolist()[0]
    return cent_and_title


# arrayで表されたベクトルの正規化
def normalize(vector):
    normalized_vector = vector / np.linalg.norm(vector)
    return normalized_vector


# 正規化しないver
def get_cluster_without_normalize(titles_df):
    features = []
    titles = []
    for k, v in titles_df.iterrows():
        features.append(v['vectorized_title'])
        titles.append(v['title'])
    cent_and_title = classify(pd.DataFrame(features))
    for i in range(len(cent_and_title)):
        cent_and_title[i][1] = pd.DataFrame(titles)[cent_and_title[i][1]].T.as_matrix().tolist()[0]
    return cent_and_title
