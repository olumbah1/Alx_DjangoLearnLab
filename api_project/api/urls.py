from django.urls import path, include
from .views import BookViewSet,BookList
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
        path('api/token/', obtain_auth_token, name='api_token_auth'),
     # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('api/', include(router.urls)), # This includes all routes registered with the router
    
]
