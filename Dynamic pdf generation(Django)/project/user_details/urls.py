from django.urls import path
from .views import user_details_view, generate_pdf

urlpatterns = [
    path('', user_details_view, name='user_details'),
    path('generate_pdf/<int:pk>/', generate_pdf, name='generate_pdf'),
]
