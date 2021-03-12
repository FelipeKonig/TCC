from django.urls import path

from apps.carrinhos.views import *

app_name = 'pedidos'

urlpatterns = [
     path('visualizar-carrinho/', visualizar_carrinho, name='visualizar_carrinho'),
     path('ajax/remover-produto-pedido/', remover_produto_pedido, name='remover_produto_pedido'),
     path('ajax/alterar-quantidade-produto-pedido/', alterar_quantidade_produto_pedido, name='alterar_quantidade_produto_pedido'),
]
