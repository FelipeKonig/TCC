from django.urls import path

from apps.produtos.views import (
     CriarProduto,
     carregar_subcategorias
)
app_name = 'produtos'

urlpatterns = [
     path('criar-produto/', CriarProduto.as_view(), name='criar_produto'),
     path('ajax/carregar-subcategoria/', carregar_subcategorias, name='ajax_carregar_subcategorias')
   # path('meus-produtos/', listar_vitrin, name='meus_produtos'),
    #path('editar-vitrine/<int:pk>', EditarVitrine.as_view(), name='editar_vitrine'),
   # path('editar-produto/', editar_vitrine, name='editar_produto'),
    #path('deletar-produto/', deletar_vitrine, name='deletar_produto')
]
