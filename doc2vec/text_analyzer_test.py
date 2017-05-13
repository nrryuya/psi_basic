# -*- coding: utf-8 -*-
"""
Created on Sat May 13 12:39:54 2017

@author: 慧
"""
import numpy as np
from numpy.linalg import norm
#もう一つのソースコード
from text_analyzer import converter 

#初期学習に必要なデータ例
title_dirs = ["I_am_a_cat.txt","run_Melos.txt"]

#初期化
conv = converter(title_dirs)

#そのモデルからの、ベクトルの生成
print("\"cat.txt:\"\n", conv.getv_dir("cat.txt") )
print("[\"にゃー\",\"我\",\"猫\",\"人\"]\n", conv.getv_raw(["にゃー","我","猫","人"]) )


#
#以下、読まなくてもいい実験
#
if 0:
    #コサイン類似度を計算
    def cos_simi(np_a1,np_a2):
        return (np_a1*np_a2).sum()/(norm(np_a1)*norm(np_a2))
    
    ###コサイン類似度の計算
    #numpyのベクトルとして分散表現を受け取る
    np_cat = np.array(conv.getv_raw(["にゃー","我","猫","人間"]))
    np_cat_mock = np.array(conv.getv_raw(["にゃー","我","人間","パンダ","チンパンジー"]))
    np_diff = np.array(conv.getv_raw(["カレーパン","チンパンジー","ウェブ開発","メロス","激怒"]))
    
    
        
    print("cos similarity(同じデータ):",cos_simi(np_cat,np_cat))
    print("cos similarity(似たデータ):",cos_simi(np_cat,np_cat_mock))
    print("cos similarity(関係ないデータ):",cos_simi(np_cat,np_diff))