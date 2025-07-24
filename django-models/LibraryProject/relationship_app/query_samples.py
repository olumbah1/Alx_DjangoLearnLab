from relationship_app.models import Author, Book, Library, Librarian
# 1. Query all books by specifying the author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        books= author.books.all()
        return [book.title for book in books]
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")

# 2. List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = Book.objects.filter(library_book=library) 
        books = library.books.all()
        return [book.title for book in books]
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")

# Retrieve the Librarian for a library
def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian.name
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}' library")

        