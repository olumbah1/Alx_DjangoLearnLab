from django.urls import path
from .views import NotificationListAPIView, MarkNotificationReadAPIView

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notifications-list'),
    path('<int:pk>/mark-read/', MarkNotificationReadAPIView.as_view(), name='notification-mark-read'),
]
