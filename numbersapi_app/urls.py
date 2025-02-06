from django.urls import path
from . import views

urlpatterns = [
    path('number/', views.number_details, name='number_details'),
]
