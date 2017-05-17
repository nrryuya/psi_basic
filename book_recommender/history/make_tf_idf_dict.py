from np_scraper import login_np
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import MeCab
from history import Article


# m = MeCab.Tagger(MECAB_PATH)
# model = gensim.models.KeyedVectors.load_word2vec_format('model.vec', binary=False)


def save_np_articles():
    driver = login_np()
    # NOTE: ここに処理をかく


def save_separated_text():
    articles = Article.objects.all()
    for article in articles:
        separated_text = m.parse(article.title + article.content)
        article.separated_text = ','.join(separated_text)
        article.save()


def make_tf_idf_dict():
    separated_texts = Article.objects.values_list('separated_text', flat=True)
    # 分かち書きに戻す
    docs = map(lambda x: x.split(','), separated_texts)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(docs)
    joblib.dump(vectorizer, 'tf_idf_model.pkl')
