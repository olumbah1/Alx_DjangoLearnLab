<!-- Create Book Instance -->
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", year=1949)

<!-- Output: -->
<Book: Book object (1)>