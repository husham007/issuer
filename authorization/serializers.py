from rest_framework import serializers
from . import models


class Authorization_presentmentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'message_type', 'card_id', 'transaction_id',
                 'merchant_name', 'merchant_city', 'merchant_country',
                 'merchant_mcc', 'billing_amount', 'billing_currency',
                 'transaction_amount', 'transaction_currency',
                 'settlement_amount', 'settlement_currency')
        model = models.Authorization_presentment

class TransfersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'card_id', 'transaction_id','account_name',
                 'entry_type', 'amount', 'currency', 'status')
        model = models.Transfers