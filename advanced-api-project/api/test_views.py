# api/test_views.py

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(user=self.user, name='Test Author')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
        self.book = Book.objects.create(
            
           title='Test Book',
           publication_year=2023,
           author=self.author
        )
   
        # URLs for API endpoints
        self.book_list_url = reverse('book-list')    # Adjust based on your urls.py name
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.book_create_url = reverse('book-create')
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book.pk})

    def test_list_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)  # At least one book returned

    def test_create_book(self):
        data = {
        'title': 'New Book',
        'publication_year': 2022,
        'author': self.author.id  # Fix
    }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        data = {
            'title': 'Updated Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.put(reverse('book-update', kwargs={'pk': self.book.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


    def test_unauthenticated_create(self):
        self.client.logout()  # Remove authentication
        response = self.client.post(self.book_create_url, {
            'title': 'Unauthorized Book',
            'publication_year': 2022
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Example of filtering test (if filtering implemented in view)
    def test_filter_books_by_publication_year(self):
        response = self.client.get(self.book_list_url + '?publication_year=2023')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for book in response.data:
            self.assertEqual(book['publication_year'], 2023)


