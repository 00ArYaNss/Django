from django.urls import path
from .views import PineconeHandler

urlpatterns = [
    path('process/', PineconeHandler.as_view(), name='process'),
]
