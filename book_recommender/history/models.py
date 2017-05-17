from django.db import models
from django.utils import timezone


# Create your models here.
class Book(models.Model):

    class Meta:
        db_table = 'books'
    name = models.CharField(max_length=250)
    text = models.TextField()

    # 書籍データの分散表現のリストを文字列にして保存
    vector = models.TextField(null=True, blank=True)

    # RakutenのURLのリンク
    # URLに日本語が含まれておりURLFieldだとオーバーすることがある？
    rakuten_url = models.TextField()

    # カテゴリ（ナイーブベイズにより分類）
    # category = models.CharField(max_length=50)

    # カテゴリ（Rakutenのカテゴリ）
    rakuten_category = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


# NewsPicksの記事。主にtf-idf用。
# class Article(models.Model):
#
#     class Meta:
#         db_table = 'articles'
#     title = models.CharField("タイトル", max_length=255)
#     url = models.URLField()
#     content = models.TextField()
#     # タイトルと本文を合体した文字列の分かち書きのリストを文字列にして保存
#     separated_text = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return self.title
