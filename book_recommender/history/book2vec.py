from history.models import Book
from user2vec import text2vec


def save_book_vector():
    books = Book.objects.all()
    for book in books:
        # TODO: 【内容情報】（出版社より）とか除いたり、内容情報と目次と著者情報で重み付け変えたりする
        vector = text2vec(book.name + book.text)
        book.vector = ','.join(vector)
        book.save()
        print("saved：" + book.name)
