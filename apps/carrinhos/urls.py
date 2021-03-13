from django.urls import path

from apps.carrinhos.views import *

app_name = 'pedidos'

urlpatterns = [
     path('visualizar-carrinho/', visualizar_carrinho, name='visualizar_carrinho'),
     path('adicionar-produto-carrinho/', adicionar_produto_carrinho, name='adicionar_produto_carrinho'),
     path('listar-pedidos/', listar_pedidos, name='listar_pedidos'),
     path('ajax/remover-produto-pedido/', remover_produto_pedido, name='remover_produto_pedido'),
     path('ajax/alterar-quantidade-produto-pedido/', alterar_quantidade_produto_pedido, name='alterar_quantidade_produto_pedido'),
]
