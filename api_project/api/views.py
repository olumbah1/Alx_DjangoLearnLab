from rest_framework import generics,viewsets,status
from .serializers import BookSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Book


# List all books – accessible by authenticated users
class BookList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    serializer_class = BookSerializer  
    queryset = Book.objects.all()      


# ViewSet for admin users to manage books (CRUD)
class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     