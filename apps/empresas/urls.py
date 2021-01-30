from django.urls import path

from .views.empresa import *
from .views import endereco
from .views import empresa

app_name = 'empresas'

urlpatterns = [
    path('criar-empresa/', CriarEmpresa.as_view(), name='criar_empresa'),
    path('minha-empresa/', empresa.empresa_perfil, name='empresa_perfil'),
    path('deletar-empresa/<int:pk>', deletar_empresa, name='deletar_empresa'),
    path('editar-empresa/<int:pk>', EditarEmpresa.as_view(), name='editar_empresa'),
    path('empresa/endereco', endereco.empresa_endereco, name='empresa_endereco'),
    path('empresa/endereco/adicionar', endereco.adicionar_endereco, name='empresa_endereco_adicionar'),
    path('empresa/endereco/editar', endereco.editar_endereco, name='editar_endereco'),
    path('empresa/endereco/deletar', endereco.deletar_endereco, name='deletar_endereco'),
    path('empresa/endereco/definir-endereco-padrao', endereco.definir_endereco_padrao, name='definir_endereco_padrao')
]
