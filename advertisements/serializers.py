from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context['request'].method
        user = self.context['request'].user
        status = AdvertisementStatusChoices.OPEN

        # TODO: добавьте требуемую валидацию
        # Проверка перед созданием нового объявления пользователем, что количество принадлежащих ему
        # объявлений со статусом "OPEN" >= 10
        if request == "POST":
            if Advertisement.objects.filter(creator=user, status=status).count() >= 10:
                raise serializers.ValidationError("Запрещено создавать более 10 открытых объявлений")

        # Проверка перед изменением статуса объявления на "OPEN" пользователем, что количество принадлежащих ему
        # объявлений со статусом "OPEN" >= 10. Изменять другие поля можно без ограничений.
        if request in ('PATCH', 'PUT') and data.get('status') == 'OPEN':
            if Advertisement.objects.filter(creator=user, status=status).count() >= 10:
                raise serializers.ValidationError("Запрещено создавать более 10 открытых объявлений")

        return data
