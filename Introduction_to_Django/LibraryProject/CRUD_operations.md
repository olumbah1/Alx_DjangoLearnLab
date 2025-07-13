<!-- Create Book Instance -->
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", year=1949)

<!-- Output: -->
<Book: Book object (1)>

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

<!-- Update the book instance -->
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book

<!-- Output: -->
<Book: Book object (1)>

<!-- Delete book instance -->
book = Book.objects.get(title="1984")
book.delete()

<!-- Output: -->
(1, {'bookshelf.Book': 1})

<!-- To retrieve after deleting -->
Book.objects.all()

<!-- Output: -->
<QuerySet []>

<!-- means: ✅ No error — but ❗ there are no Book records in the database yet. -->