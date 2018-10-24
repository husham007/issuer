from django.db import models

# Create your models here.

class Authorisation_presentment(models.Model):
    #title                = models.CharField(max_length=50)
    #balance              = models.DecimalField(max_digits=10, decimal_places=2)
    #currency             = models.CharField(max_length=3)
    message_type         = models.CharField(max_length=15)
    card_id              = models.CharField(max_length=15)
    transaction_id       = models.CharField(max_length=15)
    merchant_name        = models.CharField(max_length=15)
    merchant_city        = models.CharField(max_length=15)
    merchant_country     = models.CharField(max_length=15)
    merchant_mcc         = models.CharField(max_length=15)
    billing_amount       = models.DecimalField(max_digits=10, decimal_places=2)
    billing_currency     = models.CharField(max_length=3)
    transaction_amount   = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_currency = models.CharField(max_length=3)
    settlement_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    settlement_currency  = models.CharField(max_length=3)
    #content = models.TextField()
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_type