from django.urls import path

from .views import (
    CriarEmpresa
)

app_name = 'empresas'

urlpatterns = [
    path('criar-empresa', CriarEmpresa.as_view(), name='criar_empresa'),
]
