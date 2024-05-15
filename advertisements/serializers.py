from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices

MAX_OPEN_ADV_CNT_PER_USER = 10

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
                    'status', 'created_at', )

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

        if data.get('status', Advertisement._meta.get_field('status').default) \
                == AdvertisementStatusChoices.OPEN:
            usr_open_adv_cnt = Advertisement.objects.filter(
                status=AdvertisementStatusChoices.OPEN,
                creator=self.context["request"].user
            ).count()
            if usr_open_adv_cnt >= MAX_OPEN_ADV_CNT_PER_USER:
                raise serializers.ValidationError(
                    f'User can have maximum {MAX_OPEN_ADV_CNT_PER_USER} open advertisements.'
                )

        return data
