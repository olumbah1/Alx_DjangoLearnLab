from django_filters import rest_framework
from rest_framework import generics,filters
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User



# Create your views here.

# ListView – Retrieve all books (public access)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read
    filter_backends = [DjangoFilterBackend,
                      filters.SearchFilter,
                      filters.OrderingFilter]
    filter_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']

# DetailView – Retrieve single book by ID (public access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CreateView – Add a new book (only authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users

    def perform_create(self, serializer):
        author = Author.objects.get(user=self.request.user)
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
