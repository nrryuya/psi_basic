from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^send_account/$', views.send_account, name='send_account'),  # NewsPicksアカウントURLのPOST
    url(r'^recommend_books/$', views.recommend_books, name='recommend_books'),  # おすすめ書籍の表示
]
