from rest_framework import serializers
from mailings.models import Mailing

class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at')
