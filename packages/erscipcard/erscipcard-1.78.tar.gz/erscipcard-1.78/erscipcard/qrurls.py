from django.urls import path
from . import qrviews

urlpatterns = [
    path('', qrviews.qr ),
    path('qr/<str:text>', qrviews.qrtext ),   
]
