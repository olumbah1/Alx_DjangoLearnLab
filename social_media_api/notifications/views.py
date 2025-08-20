from .serializers import NotificationSerializer
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from .models import Notification
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
class NotificationListAPIView(ListAPIView):  # API view to list notifications for the logged-in user
    serializer_class = NotificationSerializer  # Use NotificationSerializer for output
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    
    def get_queryset(self):  # Define queryset to fetch notifications for current user
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')  # Notifications for user, newest first

class MarkNotificationReadAPIView(APIView):  # API view to mark a notification as read
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def post(self, request, pk):  # Handle POST request with notification ID (pk)
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)  # Get notification or 404 if not found or not recipient
        notification.is_read = True  # Mark notification as read
        notification.save()  # Save changes to DB
        return Response({'detail': 'Marked as read'})  # Return success message

    