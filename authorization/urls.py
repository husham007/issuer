from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('batch/', views.batch, name='batch_process'),
    #path('all/', views.Authorization_presentmentList.as_view()),
    #path('<int:pk>/', views.Authorization_presentmentDetail.as_view()),
]