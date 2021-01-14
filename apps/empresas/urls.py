from django.urls import path

from .views import (
    CriarEmpresa,
    ListarEmpresas,
    deletar_empresa
)

app_name = 'empresas'

urlpatterns = [
    path('criar-empresa/', CriarEmpresa.as_view(), name='criar_empresa'),
    path('minha-empresa/', ListarEmpresas.as_view(), name='listar_empresas'),
    path('deletar-empresa/<int:pk>', deletar_empresa, name='deletar_empresa'),
]
