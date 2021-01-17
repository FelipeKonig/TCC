from django.urls import path

from .views import (
    CriarEmpresa,
    ListarEmpresa,
    deletar_empresa,
    EditarEmpresa
)

app_name = 'empresas'

urlpatterns = [
    path('criar-empresa/', CriarEmpresa.as_view(), name='criar_empresa'),
    path('minha-empresa/', ListarEmpresa.as_view(), name='listar_empresas'),
    path('deletar-empresa/<int:pk>', deletar_empresa, name='deletar_empresa'),
    path('editar-empresa/<int:pk>', EditarEmpresa.as_view(), name='editar_empresa'),
]
