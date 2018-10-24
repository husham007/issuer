from rest_framework import serializers
from . import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'balance', 'currency')
        model = models.Account