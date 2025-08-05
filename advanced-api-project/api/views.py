
from rest_framework import generics
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

# ListView – Retrieve all books (public access)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Anyone can read


# DetailView – Retrieve single book by ID (public access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


# CreateView – Add a new book (only authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def perform_create(self, serializer):
        author = Author.objects.get(user=self.request.user)  # Get linked Author
        serializer.save(author=author)  # Assign logged-in author to book


# UpdateView – Modify a book (only authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)


# DeleteView – Remove a book (only authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
