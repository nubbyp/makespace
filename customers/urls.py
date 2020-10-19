from django.urls import path

from . import views

urlpatterns = [
    path('get_next_billing', views.get_next_billing, name='get_next_billing'),
]