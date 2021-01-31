import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from apps.produtos.forms import CriarProdutoForm
from apps.usuarios.models import CustomUsuario
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def retorna_categorias():
    categorias = 'https://api.mercadolibre.com/sites/MLB/categories#json'
    requisicao_categorias = requests.get(categorias)

    try:
        lista = requisicao_categorias.json()

    except ValueError:
        logger.critical("Não encontrou as subcategorias")

    dicionario = {}
    for indice, estados in enumerate(lista):
        dicionario[indice] = estados

    return dicionario




class CriarProduto(LoginRequiredMixin, CreateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        form = super().get_form(CriarProdutoForm)
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        dict_categorias = retorna_categorias()
        # print(dict_categorias)
        context = {
            'form': form,
            'usuario': usuario_logado,
            'categorias': dict_categorias
        }
        return render(request, 'produtos/produto_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        pass


def carregar_subcategorias(request):
    print(request.GET.get('categoria'))
    subcategorias = 'https://api.mercadolibre.com/categories/' + request.GET.get('categoria')

    requisicao_subcategorias = requests.get(subcategorias)

    try:
        lista = requisicao_subcategorias.json()

    except ValueError:
        logger.critical("Não encontrou as subcategorias")

    lista_subcategorias = lista['children_categories']

    dicionario = {}
    for indice, subcategoria in enumerate(lista_subcategorias):
        # apenas filtrando os dados do objeto em cidades para pegar apenas o nome,
        # dessa forma facilita a manipulação dos dados com js
        dicionario[indice] = subcategoria.get('name')

    if request.is_ajax():
        return JsonResponse({'subcategorias': dicionario})
