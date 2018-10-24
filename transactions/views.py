import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view
from .models import Authorisation_presentment
from django.db.models import Sum
from .serializers import Authorisation_presentmentSerializer

# Create your views here.


class Authorisation_presentmentList(generics.ListCreateAPIView):
    queryset = Authorisation_presentment.objects.all()
    serializer_class = Authorisation_presentmentSerializer


class Authorisation_presentmentDetail(generics.RetrieveAPIView):
    queryset = Authorisation_presentment.objects.all()
    serializer_class = Authorisation_presentmentSerializer

class Authorisation_presentmentP(generics.ListAPIView):    
    serializer_class = Authorisation_presentmentSerializer
    
    def get_queryset(self):
        card_id = self.kwargs['card_id']
        return Authorisation_presentment.objects.filter(message_type = 'presentment', card_id = card_id)

@api_view(['GET'])
def authorised_amount(request, card_id):
   
    reserved_amounts= Authorisation_presentment.objects.filter(card_id = card_id, 
                                                                message_type = 'authorisation'
                                                                ).aggregate(Sum('billing_amount'))

    if request.method == 'GET':
       return Response(reserved_amounts)

@api_view(['POST'])
def settle(request):

    card_id = request.data['card_id']
    transaction_id = request.data['transaction_id']

    #reserved_amounts= Authorisation_presentment.objects.filter(card_id = card_id).aggregate(Sum('billing_amount'))
    authorisation = Authorisation_presentment.objects.get(card_id = card_id,
                                                transaction_id = transaction_id,
                                                message_type ='authorisation')
    authorisation.message_type = 'authorisation_settled'
    authorisation.save()

    presentment = Authorisation_presentment.objects.get(card_id = card_id,
                                                transaction_id = transaction_id,
                                                message_type ='presentment')
    presentment.message_type = 'presentment_settled'
    presentment.save()

    if authorisation and presentment:
        return Response(True)
    

 