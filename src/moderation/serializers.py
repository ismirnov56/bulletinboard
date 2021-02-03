from rest_framework import serializers

from src.moderation.models import Moderation


class ModerationSerializer(serializers.ModelSerializer):
    """
        Сериализатор для модерации
    """
    class Meta:
        model = Moderation
        fields = ['id', 'user', 'announcement', 'status', 'info_result']

    def save(self, **kwargs):
        """
            Проверяем статусы, если статутс объявления не на модерации, то выбрасываем исключени
            Если статус верный, то в зависимости от присвоенного статуса модератором производим
            изменения в объявлении
        """
        announcement = self.validated_data['announcement']
        status = self.validated_data['status']
        if announcement.status != 'on_moderation':
            raise serializers.ValidationError({'announcement':'Announcement has bad status'})
        if status == 'publish':
            announcement.status = 'active'
        else:
            announcement.status = 'rejected'
        announcement.save()
        return super().save(**kwargs)


class ModerationResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moderation
        fields = ['id', 'status', 'info_result']