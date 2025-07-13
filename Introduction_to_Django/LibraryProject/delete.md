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