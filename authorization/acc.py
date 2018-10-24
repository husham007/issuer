import requests
from rest_framework.response import Response
from rest_framework.views import status
from .models import Authorization_presentment, Transfers
from django.db.models import Sum


###################################################################

def check_bal(request):

    base_url = 'http://127.0.0.1:8000/accounts/'

    if  request.method == 'POST':
        data = request.data
        billing_amount=data['billing_amount']
        print (billing_amount)

        #base_url = 'http://127.0.0.1:8000/api/'
        url = base_url + data['card_id']+'/'
        response = requests.get(url)
        account_data = response.json()
        #task = account_data
        if 'balance' in account_data:
            balance = float (account_data['balance'])
            print ('balance', balance)
            total_reserve_amount = reservations_sum(request)
            print ('all reservations',total_reserve_amount)
        else:
            return False

        if total_reserve_amount is None:
            working_balance = balance
        else:
            working_balance = balance - float (reservations_sum(request))

        print ('working balance', working_balance)
        print ('all reservations',total_reserve_amount)

        if working_balance >= float (billing_amount):
            return True
        else:
            return False
#################################################################
        
def reservations_sum(request):
    if  request.method == 'POST':
        data = request.data
        card_id = data['card_id']
        billing_amount = data['billing_amount']  

        base_url = 'http://127.0.0.1:8000/transaction/authorised/'
        url = base_url + data['card_id']+'/'
      
        response = requests.get(url)
        data = response.json()

        print (data)
        return data['billing_amount__sum']    
        
###################################################################

def create_reservation(request):

    data = request.data
    url = 'http://127.0.0.1:8000/transaction/'
    

    return requests.post(url, json={
            'message_type': data['type'],
            'card_id': data['card_id'],
            'transaction_id': data['transaction_id'],
            'merchant_name': data['merchant_name'],
            'merchant_city': '0',
            'merchant_country': data['merchant_country'],
            'merchant_mcc': data['merchant_mcc'],
            'billing_amount': data['billing_amount'],
            'billing_currency': data['billing_currency'],
            'transaction_amount': data['transaction_amount'],
            'transaction_currency': data['transaction_currency'],
            'settlement_amount': '0',
            'settlement_currency': '0',
         })

###################################################################

def create_presentment(request):
        
    data = request.data
    url = 'http://127.0.0.1:8000/transaction/'
    

    presentment = requests.post(url, json={
                    'message_type': data['type'],
                    'card_id': data['card_id'],
                    'transaction_id': data['transaction_id'],
                    'merchant_name': data['merchant_name'],
                    'merchant_city': data['merchant_city'],
                    'merchant_country': data['merchant_country'],
                    'merchant_mcc': data['merchant_mcc'],
                    'billing_amount': data['billing_amount'],
                    'billing_currency': data['billing_currency'],
                    'transaction_amount': data['transaction_amount'],
                    'transaction_currency': data['transaction_currency'],
                    'settlement_amount': data['settlement_amount'],
                    'settlement_currency': data['settlement_currency'],
         })

    if presentment:
        if make_enteries(data):
            return True
        else:
            return False
    else:
        return False   
###################################################################

def make_enteries(data):
    print ('make_enteires')
    revenue = float (data['billing_amount']) - float (data['settlement_amount'])
    print (revenue)

    if revenue > 0:
        make_entry(data, data['billing_amount'],'customer_purchases', 'debit')       
        make_entry2( data['settlement_amount'],data['settlement_currency'],
                    'payable_to_scheme', 'credit', 'new')  

        make_entry(data, data['billing_amount'],'customer_liabilities', 'debit')
        make_entry(data, data['billing_amount'],'customer_funds', 'credit')

        make_entry2(revenue,data['settlement_currency'], 'revenue', 'credit', ' ')
        
        return True

    else:
        return False
###################################################################

def make_entry(data, amount, account_name, entry_type):

    return Transfers.objects.create(
                            card_id        = data['card_id'],
                            transaction_id = data['transaction_id'],
                            account_name   = account_name,
                            entry_type     = entry_type,
                            amount         = amount,
                            currency       = data['billing_currency'],
                            status = ''        
                        )
###################################################################
                        
def make_entry2(amount, currency, account_name, entry_type, status):

    return Transfers.objects.create(
                            card_id        = 0,
                            transaction_id = 0,
                            account_name   = account_name,
                            entry_type     = entry_type,
                            amount         = amount,
                            currency       = currency,
                            status         = status        
                        )

###################################################################

def deduct_customer_expenses(request):
    amount  = request.data['billing_amount'] 
    card_id = request.data['card_id']
    url = 'http://127.0.0.1:8000/accounts/'+ card_id + '/'

    response = requests.get(url)
    data = response.json()
    new_balance = float (data['balance']) - float (amount)
    requests.patch(url, json={
         'balance': str(new_balance),
    })
###################################################################

def settle(request):
     card_id = request.data['card_id']
     transaction_id = request.data['transaction_id']
     url = 'http://127.0.0.1:8000/transaction/settle/'
     
     requests.post(url,json={
                    'card_id'        : card_id,
                    'transaction_id' : transaction_id,
    })
###################################################################

def run_batch_process():
    total_payables = Transfers.objects.filter(
                        account_name = 'payable_to_scheme',
                        entry_type = 'credit',
                        status = 'new'
                        ).aggregate(Sum('amount'))
    """
    all_payable_debits = Transfers.objects.filter(
                            account_name = 'payable_to_scheme',
                            entry_type = 'debit').aggregate(Sum('amount'))
    """
    payables = total_payables['amount__sum']
    if payables is not None:
        if make_entry2(payables, 'EUR', 'payable_to_scheme', 'debit', 'settled'): 
            if make_entry2(payables, 'EUR', 'assets_bank', 'credit', 'settled'):
                settle_payables()
                return True
            else:
                return False
        return False
    return False
###################################################################

def settle_payables():
    Transfers.objects.filter(account_name ='payable_to_scheme',
                            status = 'new').update(status='settled')

def account_balance(account_name):
    debits_sum = Transfers.objects.filter(
                        account_name = account_name,
                        entry_type = 'debit').aggregate(Sum('amount'))

    credits_sum = Transfers.objects.filter(
                        account_name = account_name,
                        entry_type = 'credit').aggregate(Sum('amount'))


    total_debits = debits_sum['amount__sum']
    total_credits = credits_sum['amount__sum']

    print ('total_debits', total_debits )
    print ('total_credits', total_credits )

    if total_credits is not None:
        if total_debits is not None:
            return str (abs(total_debits - total_credits))
        else:
            return str (total_credits)
    else:
        if total_debits is not None:
            return str (total_debits) 


    """
    total_credits = all_payable_credits['amount__sum']
    total_debits = all_payable_debits['amount__sum']

    if total_credits is not None:
        if total_debits is not None:
            if total_credits > total_debits:
                payable_balance = total_credits - total_debits
            else:
                payable_balance = 0
        else:
            payable_balance = total_credits
    else:
            payable_balance = 0

    if payable_balance > 0:
        make_entry2(payable_balance, 'EUR', 'payable_to_scheme', 'debit')
        make_entry2(payable_balance, 'EUR', 'assets_bank', 'credit')     

    return payable_balance
    """

"""
        Authorization_presentment.objects.create(
        message_type         = data['type'],
        card_id              = data['card_id'],
        transaction_id       = data['transaction_id'],
        merchant_name        = data['merchant_name'],
        #merchant_city        = data['merchant_city'],
        merchant_country     = data['merchant_country'],
        merchant_mcc         = data['merchant_mcc'],
        billing_amount       = data['billing_amount'],
        billing_currency     = data['billing_currency'],
        transaction_amount   = data['transaction_amount'],
        transaction_currency = data['transaction_currency'],
        settlement_amount    = 0,
        settlement_currency  = 0   
    )
"""