from django.urls import path
from .views import BookListAPIView

urlpatterns = [
    path('Book/', BookListAPIView.as_view(), name = 'Book = book-list'),
    
]
