import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from apps.produtos.forms import CriarProdutoForm
from apps.produtos.models import (
    Categoria,
    SubCategoria,
    Produto, Caracteristica
)
from apps.usuarios.models import CustomUsuario
from django.http import JsonResponse
import logging

from apps.vitrines.models import Vitrine

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

        context = {
            'form': form,
            'usuario': usuario_logado,
            'categorias': dict_categorias
        }
        return render(request, 'produtos/produto_cadastro.html', context)

    def post(self, request, *args, **kwargs):

        form = self.get_form(CriarProdutoForm)
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        dict_categorias = retorna_categorias()
        id_categoria = request.POST.get('categoria')
        print(request.POST)
        print(form.is_valid())
        vitrine = Vitrine.objects.filter(vendedor=usuario_logado, status=True).first()

        print(type(vitrine))
        if form.is_valid():
            nome = form.cleaned_data['nome']
            preco = form.cleaned_data['preco']
            descricao = form.cleaned_data['descricao']
            quantidade = form.cleaned_data['quantidade']
            imagem = form.cleaned_data['imagem']
            caracteristica = form.cleaned_data['caracteristica']
            categoria = buscar_categoria(id_categoria)
            subcategoria = request.POST.get('subcategoria')
            topico = form.cleaned_data['topico']

            verificar_subcategoria_vazia = False

            try:
                categoria_bd = Categoria.objects.get(nome=categoria)
            except Categoria.DoesNotExist:
                categoria_bd = Categoria.objects.create(nome=categoria)

            if subcategoria is not None:
                try:
                    subcategoria_bd = SubCategoria.objects.get(nome=subcategoria, categoria=categoria_bd)
                except SubCategoria.DoesNotExist:
                    subcategoria_bd = SubCategoria.objects.create(nome=subcategoria, categoria=categoria_bd)
            else:
                verificar_subcategoria_vazia = True

            try:

                produto = Produto.objects.get(nome=nome, preco=preco,
                                              vendedor=usuario_logado, descricao=descricao,
                                              quantidade=quantidade, imagem=imagem,
                                              categoria=categoria_bd, vitrine=vitrine
                                              )

            except Produto.DoesNotExist:
                produto = Produto.objects.create(
                    nome=nome, preco=preco,
                    vendedor=usuario_logado, descricao=descricao,
                    quantidade=quantidade, imagem=imagem,
                    categoria=categoria_bd, vitrine=vitrine
                )

            try:
                caracteristica_bd = Caracteristica.objects.get(descricao=caracteristica, topico=topico, produto=produto)
            except Caracteristica.DoesNotExist:
                caracteristica_bd = Caracteristica.objects.create(descricao=caracteristica, topico=topico, produto=produto)

            if not verificar_subcategoria_vazia:
                subcategoria_bd.save()

            categoria_bd.save()
            caracteristica_bd.save()
            produto.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('vitrines:minha_vitrine')

        else:
            messages.error(request, 'Erro ao enviar formulário!')

        context = {
            'form': form,
            'usuario': usuario_logado,
            'categorias': dict_categorias
        }
        return render(request, 'produtos/produto_cadastro.html', context)


def carregar_subcategorias(request):
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


def buscar_categoria(id):
    categoria = 'https://api.mercadolibre.com/categories/' + id

    requisicao_categoria = requests.get(categoria)

    try:
        lista = requisicao_categoria.json()

    except ValueError:
        logger.critical("Não encontrou as subcategorias")

    return lista['name']
