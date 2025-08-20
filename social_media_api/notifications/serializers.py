from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):  # Serializer for Notification model
    actor_username = serializers.CharField(source='actor.username', read_only=True)  # Get actor's username (read-only)
    target_repr = serializers.SerializerMethodField()  # Custom method field to represent target object

    class Meta:
        model = Notification  # Set model to Notification
        fields = [  # Fields included in the serialization
            'recipient',  # User receiving the notification
            'actor',      # User who performed the action
            'verb',       # Action performed description
            'timestamp',  # When the notification was created
            'actor_username',  # Actor's username (from above)
            'target_repr',     # String representation of target object
            'is_read'          # Whether notification is read or not
        ]

    def get_target_repr(self, obj):  # Method to return string representation of the target object
        return str(obj.target)  # Convert target object to string
