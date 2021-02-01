from django.urls import path

from apps.produtos.views import (
     CriarProduto,
     carregar_subcategorias,
     deletar_produto
)
app_name = 'produtos'

urlpatterns = [
     path('criar-produto/', CriarProduto.as_view(), name='criar_produto'),
     path('ajax/carregar-subcategoria/', carregar_subcategorias, name='ajax_carregar_subcategorias'),
     path('deletar-produto/', deletar_produto, name='deletar_produto')
   # path('meus-produtos/', listar_vitrin, name='meus_produtos'),
    #path('editar-vitrine/<int:pk>', EditarVitrine.as_view(), name='editar_vitrine'),
   # path('editar-produto/', editar_vitrine, name='editar_produto'),
    #
]
