from django.urls import path

from apps.produtos.views import *

app_name = 'produtos'

urlpatterns = [
     path('criar-produto/', CriarProduto.as_view(), name='criar_produto'),
     path('ajax/carregar-subcategoria/', carregar_subcategorias, name='ajax_carregar_subcategorias'),
     path('deletar-produto/', deletar_produto, name='deletar_produto'),
     path('editar-produto/', editar_produto, name='editar_produto'),
     path('visualizar-produto/', visualizar_produto, name='visualizar_produto'),
]
