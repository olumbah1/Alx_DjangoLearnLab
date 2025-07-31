<!-- Update the book instance -->
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book

<!-- Output: -->
<Book: Book object (1)>