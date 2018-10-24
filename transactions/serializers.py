from rest_framework import serializers
from . import models


class Authorisation_presentmentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'message_type', 'card_id', 'transaction_id',
                 'merchant_name', 'merchant_city', 'merchant_country',
                 'merchant_mcc', 'billing_amount', 'billing_currency',
                 'transaction_amount', 'transaction_currency',
                 'settlement_amount', 'settlement_currency')
        model = models.Authorisation_presentment