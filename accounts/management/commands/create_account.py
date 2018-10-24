from django.core.management.base import BaseCommand
from accounts.models import Account
from authorization.models import Transfers
from authorization import acc


class Command(BaseCommand):
    help = 'Create account'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Title of account')
        parser.add_argument('amount', type=int, help='amount')
        parser.add_argument('currency', type=str, help='EUR')


    def handle(self, *args, **kwargs):
        title = kwargs['title']
        amount = kwargs['amount']
        currency = kwargs['currency']

        account = Account.objects.create(title= title,
                                    balance = amount,
                                    currency = currency
                                    )

                        
        if account is not None:

            print("Acount Created with card_id = ", account.id)
            acc.make_entry2(amount, 'EUR', 'assets_bank', 'debit', ' ')

            data = {
                'card_id': account.id, 
                'transaction_id': ' ',
                'billing_currency': currency
            }
            acc.make_entry(data, amount,'customer_liabilities', 'credit')
            acc.make_entry(data, amount,'customer_funds', 'debit')

        else:
            self.stdout.write("Account is not created")