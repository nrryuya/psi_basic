import numpy as np
from history.models import Book
from history.words import ignore_words, remove_words
from history.user2vec import *


# modelとかmとかこれで動く？
def text2vec_for_book(text):
    separated_text = extract_keyword(text)
    vec = np.zeros(300)
    count = 0
    for word in separated_text:
        if not (word in ignore_words):
            try:
                # vec+= model[word] * idf_dict[word]
                vec += model[word]  # NOTE: modelにない単語はinferした方が良いかもしれない
                count += 1
            except:
                continue
    if count == 0:
        return 0
    else:
        return vec / count


def save_book_vector():
    books = Book.objects.all()
    for book in books:
        text = book.name + book.text
        for remove_word in remove_words:
            text = text.replace(remove_word, '')
        vector = text2vec_for_book(text)
        vector = vector.tolist()
        vector = list(map(str, vector))
        book.vector = ','.join(vector)
        book.save()
        print("saved：" + book.name)
