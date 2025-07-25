from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, LibraryDetailView, BookCreateView, BookUpdateView, BookDeleteView  # SignUpView from your code
from .views import admin_view, librarian_view, member_view
urlpatterns = [
    # Your app's views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
    path('register/', views.register, name='register'),

    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    path('add_book/', BookCreateView.as_view(), name='book_add'),
    path('edit_book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('delete_book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]


