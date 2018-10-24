from django.core.management.base import BaseCommand
from accounts.models import Account
from authorization import acc


class Command(BaseCommand):
    help = 'load money in account'

    def add_arguments(self, parser):
        parser.add_argument('card_holder', type=int, help='card number')
        parser.add_argument('amount', type=int, help='amount')
        parser.add_argument('currency', type=str, help='EUR')


    def handle(self, *args, **kwargs):
        id = kwargs['card_holder']
        amount = kwargs['amount']
        currency = kwargs['currency']

        try:
            account          = Account.objects.get(pk=id)
            account.balance  = account.balance + amount
            account.currency = currency
            account.save()
            
        except Account.DoesNotExist:
            account = None

        if account is not None:
            acc.make_entry2(amount, 'EUR', 'assets_bank', 'debit', '')

            data = {
                'card_id': account.id, 
                'transaction_id': ' ',
                'billing_currency': currency
            }
            acc.make_entry(data, amount,'customer_liabilities', 'credit')
            acc.make_entry(data, amount,'customer_funds', 'debit')

            self.stdout.write("Money Loaded")
        else:
            self.stdout.write("Account does not exist")