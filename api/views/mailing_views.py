from rest_framework import viewsets, permissions
from mailings.models import Mailing
from api.serializers.mailing_serializers import MailingSerializer

class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role in ['manager', 'admin']:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=user)
