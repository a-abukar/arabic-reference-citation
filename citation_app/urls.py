from django.urls import path
from . import views

urlpatterns = [
    path('', views.citation_view, name='citation_view'),
]
