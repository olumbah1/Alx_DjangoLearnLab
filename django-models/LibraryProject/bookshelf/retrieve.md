<!-- Retrieve book instance -->
book = Book.objects.get(title="1984")
print(book.title)
print(book.author)
print(book.publication_year)

<!-- Output: -->
 book = Book.objects.get(title="1984")
>>> print(book.title)
1984
>>> print(book.author)
George Orwell
>>> print(book.publication_year)
1949