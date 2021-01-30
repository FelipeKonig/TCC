from django.urls import path

from .views import (
    CriarEmpresa,
    ListarEmpresa,
    delecao_empresa,
    edicao_empresa
)

app_name = 'empresas'

urlpatterns = [
    path('criar-empresa/', CriarEmpresa.as_view(), name='criar_empresa'),
    path('minha-empresa/', ListarEmpresa.as_view(), name='listar_empresas'),
    path('deletar-empresa/', delecao_empresa, name='deletar_empresa'),
    path('editar-empresa/', edicao_empresa, name='edicao_empresa')
]
