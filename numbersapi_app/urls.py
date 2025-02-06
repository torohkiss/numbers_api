from django.urls import path
from . import views

urlpatterns = [
    path('number_details/', views.number_details, name='number_details'),
]
