from rest_framework import serializers
from mailings.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('user', 'subject', 'body', 'created_at')