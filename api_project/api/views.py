from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer
from .models import Book
# Create your views here.
class BookListAPIView(generics.ListAPIView):
    queryset = Book.object.all()
    serializer_class = BookSerializer
    
    def perform_create(self, serializer):
        serializer.save()