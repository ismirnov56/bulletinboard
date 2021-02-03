from django.core import exceptions
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import ValidationError

from src.announcement.models import Announcements
from src.base.permissions import IsStuffUser
from src.moderation.models import Moderation
from src.moderation.serializers import ModerationSerializer


class CreateModeration(CreateAPIView):
    """
    View для модератора
    Для этого достаточно передать uuid объявления
    """
    queryset = Moderation.objects.all()
    permission_classes = [IsStuffUser]
    serializer_class = ModerationSerializer
    lookup_field = 'announcement_uuid'

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        try:
            obj = Announcements.objects.get(uuid=self.kwargs['announcement_uuid'])
        except exceptions.ValidationError:
            raise ValidationError({'announcement': 'Not found announcement'})
        serializer.validated_data['announcement'] = obj
        serializer.save()
