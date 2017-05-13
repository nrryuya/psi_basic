# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:41:50 2017

@author: 慧
"""

from gensim import models
from gensim.models import doc2vec
from janome.tokenizer import Tokenizer



#指定されたテキストファイルの品詞分解(っぽいもの)
#名詞・動詞などのlistを返す
def decompose(text_dir):    
    
    text = open(text_dir, 'r').read()#txtファイル読み込み
#    text = text.replace('\n', '')    #扱いやすいstrに変換
    t = Tokenizer()
    tokens = t.tokenize(text)
    words = []
    
    for token in tokens:
        # 品詞を取り出し
        partOfSpeech = token.part_of_speech.split(',')[0]
     
        # unicode型 は str型 へ
        if isinstance(partOfSpeech, bytes):
            partOfSpeech = partOfSpeech.encode('utf-8')
        #名詞はそのまま取り出し
        if (partOfSpeech == '名詞'):
            words.append(token.surface)
        #用言は原型で取り出し
        if (partOfSpeech == '動詞') | (partOfSpeech == '形容詞')|(partOfSpeech == '形容動詞'):
            words.append(token.base_form)

    return words



#[[title,ディレクトリ],[t,デ],...]の形のリストから、
#doc2vec引数に使われるのオブジェクトに、データを変換
def dirs_to_sentences(dirs):
    ld = len(dirs)
    for i in range( ld ):    
        words0 = decompose(dirs[i])
        title = dirs[i]
        yield doc2vec.LabeledSentence(words=words0, tags=[title])

#[[title,ディレクトリ],[t,デ],...]の形のリストをもらって初期化して
#converter.getv("テキストのディレクトリ")method

class converter:
    def __init__(self,dirs,filename="converter"):
        sentences = dirs_to_sentences(dirs)
        self.model = models.Doc2Vec(sentences, dm=1, size=300, window=15, alpha=.025,
        min_alpha=.025, min_count=1, sample=1e-6)
        #print('\n訓練開始')
        for epoch in range(20):
            #print('Epoch: {}'.format(epoch + 1))
            self.model.train(sentences)
            self.model.alpha -= (0.025 - 0.0001) / 19
            self.model.min_alpha = self.model.alpha
        self.model.save('{}.model'.format(filename))
        self.model = models.Doc2Vec.load('{}.model'.format(filename))
        
    def getv_dir(self,text_dir):
        return self.model.infer_vector(decompose(text_dir))
   
    def getv_raw(self,raw_text):
        return self.model.infer_vector(raw_text)

