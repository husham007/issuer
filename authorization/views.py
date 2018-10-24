# Create your views here.

from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view
from . import acc
from .models import Authorization_presentment
from .serializers import Authorization_presentmentSerializer

#from .decorators import validate_request_data


@csrf_exempt
@api_view(['POST'])
def home(request):   
    
    if  request.method == 'POST':

            if request.data['type']=='authorisation':
                if  acc.check_bal(request):
                    if acc.create_reservation(request):
                        return  Response('OK', status=status.HTTP_200_OK)
                    else:
                        return  Response('BAD REQUEST', status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response ('FUNDS NOT AVAILABLE OR NO ACCOUNT EXIST', 
                                    status=status.HTTP_403_FORBIDDEN)

            elif request.data['type']=='presentment':
                if  acc.create_presentment(request):
                    acc.deduct_customer_expenses(request)
                    acc.settle(request)
                    return  Response('PRESENTMENT_OK', status=status.HTTP_200_OK)  
                else:
                     return Response ('BAD PRESENTMENT REQUEST', 
                                    status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response ('BAD REQUEST', status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def batch(request): 
    data = {'nothing to batch process'}
    if acc.run_batch_process():
        
        data = {
            'My assets at Bank': acc.account_balance('assets_bank'),
            'Payable to Scheme': acc.account_balance('payable_to_scheme'),
            'Liabilities to Customers': acc.account_balance('customer_liabilities'),
            'Customers Purchases': acc.account_balance('customer_purchases'),
            'Customers Funds': acc.account_balance('customer_funds'),
            'My Revenue': acc.account_balance('revenue')
        }
        print (data)
    return Response (data=data)
        



"""
    acc.check_bal(request)
    if  request.method == 'POST':
        data = request.data
        transaction=data['transaction']
        print (transaction)
        base_url = 'http://127.0.0.1:8000/api/'
        url = base_url + data['card_id']+'/'
        response = requests.get(url)
        accountdata = response.json()
        task = accountdata
        balance = float (accountdata['balance'])
        task['balance']=balance+float(transaction)
        requests.put(url, json=task)
        print (accountdata)

 """       
    #print (json.loads(request.body))
    
    #if 'username' in request.body:
    #username = request.body
    
    #data = username.json()
    #print (username)

"""
    response = requests.get(url)
    print(response.json())
    return Response('OK', status=status.HTTP_200_OK)
    


class Authorization_presentmentList(generics.ListAPIView):
    queryset = Authorization_presentment.objects.all()
    serializer_class = Authorization_presentmentSerializer


class Authorization_presentmentDetail(generics.RetrieveAPIView):
    queryset = Authorization_presentment.objects.all()
    serializer_class = Authorization_presentmentSerializer
"""