from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Todo serializer"""
    is_completed = serializers.BooleanField(source='completed')
    created = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'is_completed', 'created', 'updated_at']
        read_only_fields = ['created', 'updated_at']