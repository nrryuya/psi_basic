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

    # AmazonのURLのリンク（例：https://www.amazon.co.jp/gp/product/4046029161/）
    amazon_url = models.URLField()

    # カテゴリ（ナイーブベイズにより分類）
    # category = models.CharField(max_length=50)

    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
