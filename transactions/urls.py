from django.urls import path
from . import views

urlpatterns = [
    path('authorised/<int:card_id>/', views.authorised_amount, name='home'),
    path('', views.Authorisation_presentmentList.as_view()),
    #path('all/', views.Authorisation_presentmentList.as_view()),
    path('settle/', views.settle, name = 'settle'),
    path('presentment/<int:card_id>/', views.Authorisation_presentmentP.as_view()),
]