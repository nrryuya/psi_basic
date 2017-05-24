
# coding: utf-8

# In[1]:

# Author: Thierry Guillemot <thierry.guillemot.work@gmail.com>
# License: BSD 3 clause

import numpy as np
import pandas as pd

from sklearn.mixture import BayesianGaussianMixture
from sklearn.decomposition import PCA


# In[2]:
# サンプルデータの読み込み
import re

data0 = pd.read_csv("ryuya's_picked_articles")
data0.head()

# 文字列をリストに起こす


def enlist(str_list):
    divided_list = re.findall("[-0-9.]+", str(str_list))
    float_list = []
    for i in range(len(divided_list)):
        float_list.append(float(divided_list[i]))
    return float_list

# 所定の形式のデータの変形→list1に格納
list0 = np.array(enlist(data0.vectorized_title[0]))
list0 + np.random.standard_normal(300)
list1 = []
for i in range(50):
    list1.append(["title" + str(i), (list0 + np.random.standard_normal(300)).tolist()])


# 以下クラスの定義

# In[24]:

class title_likelihood:

    def fit(self, list1):
        # titleとfeatureのリストに分離
        features = []
        for i in range(len(list1)):
            features.append(list1[i][1])
        self.n_cluster = max(20, int(len(list1) / 3) + 2)

        # 次元圧縮
        pca = PCA(n_components=50)
        self.pca_model = pca.fit(pd.DataFrame(features))
        pca_features = self.pca_model.transform(pd.DataFrame(features))

        # 訓練されたGMMモデル
        self.dpgmm = BayesianGaussianMixture(
            n_components=self.n_cluster, covariance_type='full', weight_concentration_prior=1e+2,
            weight_concentration_prior_type='dirichlet_process',
            mean_precision_prior=1e-2, covariance_prior=1e0 * np.eye(50),
            init_params="kmeans", max_iter=100, random_state=2).fit(pca_features)

        # 各クラスター(各ガウス分布)の重みづけ、
        self.covs = self.dpgmm.covariances_
        self.mus = self.dpgmm.means_
        self.pis = self.dpgmm.weights_

    def predict(self, list1):

        # titleとfeatureのリストに分離
        features = []
        titles = []
        for i in range(len(list1)):
            features.append(list1[i][1])
            titles.append(list1[i][0])

        # ガウス分布内でのp値を取得する
        def mnd(_x, _mu, _sig):
            x = np.matrix(_x)
            mu = np.matrix(_mu)
            sig = np.matrix(_sig)
            a = np.sqrt(np.linalg.det(sig) * (2 * np.pi)**sig.ndim)
            b = np.linalg.det(-0.5 * (x - mu) * sig.I * (x - mu).T)
            return np.exp(b) / a

        # 個別のfeatureに対して、尤度を求める
        # 引数はpd.dataframe形式の、vector
        def predict_likelihood(nf):
            likelihood = 0
            for i in range(self.n_cluster):
                likelihood += self.pis[i] * mnd(nf, self.mus[i], self.covs[i])
            return likelihood

        # featureの並んだ、データフレームに対して、それぞれの尤度を求める
        def predict_l_features(new_features):
            nfs = self.pca_model.transform((new_features))
            ll_nfs = np.apply_along_axis(predict_likelihood, axis=1, arr=nfs)
            return ll_nfs

        # 各データの尤度を求め、
        likelihood_nfs = predict_l_features(pd.DataFrame(features))

        pd_title_likelihood = pd.DataFrame(titles)
        pd_title_likelihood["likelihood"] = likelihood_nfs
        pd_title_likelihood.columns = ["title", "likelihood"]
        pd_title_likelihood = pd_title_likelihood.sort_values(by="likelihood")
        pd_title_likelihood.index = range(len(pd_title_likelihood))

        return pd_title_likelihood


# 使い方：title_likelihoodのインスタンスを作る
# fitで所定型の学習用データ(Picks)をフィード
# predictで同じ形のデータ(本のタイトルと分散表現)を入れる→尤度(空間上での確率密度)が返ってくる

# In[25]:

tl = title_likelihood()


# In[26]:

tl.fit(list1)


# In[27]:

print(tl.predict(list1))
