from django.urls import path
from .views import ImportarDadosView

urlpatterns = [
    path('', ImportarDadosView.as_view(), name='importar_dados'), 
]