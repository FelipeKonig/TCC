import requests
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from apps.produtos.forms import (
    CriarProdutoForm,
    EditarProduto
)
from apps.produtos.models import *
from apps.usuarios.models import CustomUsuario
from django.http import JsonResponse

from apps.vitrines.models import Vitrine

logger = logging.getLogger(__name__)

recuperar_id_editar_produto = {}
recuperar_id_deletar_produto = {}

def retorna_categorias():
    categorias = 'https://api.mercadolibre.com/sites/MLB/categories#json'
    requisicao_categorias = requests.get(categorias)

    try:
        lista = requisicao_categorias.json()

    except ValueError:
        logger.critical("Não encontrou as subcategorias")

    dicionario = {}
    for indice, categorias in enumerate(lista):
        dicionario[indice] = categorias

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
        nome_categoria = request.POST.get('categoria').split('|')[0]
        vitrine = Vitrine.objects.filter(vendedor=usuario_logado, status=True).first()

        if form.is_valid():

            nome = form.cleaned_data['nome']
            preco = form.cleaned_data['preco']
            descricao = form.cleaned_data['descricao']
            quantidade = form.cleaned_data['quantidade']
            categoria = buscar_categoria_bd(nome_categoria)

            novo_produto = Produto.objects.create(
                nome=nome,
                preco=preco,
                descricao=descricao,
                quantidade=quantidade,
                categoria=categoria,
                vitrine=vitrine
            )

            if request.POST.get('subcategoria'):
                logger.debug(request.POST.get('subcategoria'))
                subcategoria = buscar_subcategoria_bd(categoria, request.POST.get('subcategoria'))

                novo_produto.subCategoria = subcategoria
                novo_produto.save()

            adicionar_caracteristicas_produto(request.POST, novo_produto)

            imagens_produto = request.FILES.getlist('foto')

            index = 0
            while index < len(imagens_produto):

                nova_imagem = ImagemProduto.objects.create(
                    imagem = imagens_produto[index],
                    produto = novo_produto
                )
                nova_imagem.save()
                index += 1

            return redirect('vitrines:minha_vitrine')
        else:
            messages.error(request, 'Erro ao enviar formulário!')

        dict_categorias = retorna_categorias()
        context = {
            'form': form,
            'usuario': usuario_logado,
            'categorias': dict_categorias
        }
        return render(request, 'produtos/produto_cadastro.html', context)


def carregar_subcategorias(request):

    categoria = request.GET.get('categoria').split('|')[-1]
    logger.debug(categoria)
    subcategorias = 'https://api.mercadolibre.com/categories/' + categoria

    requisicao_subcategorias = requests.get(subcategorias)

    try:
        lista = requisicao_subcategorias.json()

    except ValueError:
        logger.critical("Não encontrou as subcategorias")

    lista_subcategorias = lista['children_categories']

    dicionario = {}
    for indice, subcategoria in enumerate(lista_subcategorias):
        dicionario[indice] = subcategoria.get('name')

    if request.is_ajax():
        return JsonResponse({'subcategorias': dicionario})


def buscar_categoria_bd(nome):

    categoria_bd = Categoria.objects.get_or_create(nome=nome)
    categoria_bd = Categoria.objects.get(nome=nome)
    return categoria_bd

def buscar_subcategoria_bd(categoria, subcategoria):

    subcategoria_bd = SubCategoria.objects.get_or_create(nome=subcategoria, categoria=categoria)
    subcategoria_bd = SubCategoria.objects.get(nome=subcategoria, categoria=categoria)
    return subcategoria_bd

@login_required(login_url='/usuarios/login')
def editar_produto(request):

    if not recuperar_id_editar_produto:
        recuperar_id_editar_produto['id'] = request.POST.get('id')

    produto = retornar_produto()
    usuario_logado = CustomUsuario.objects.get(email=request.user)
    caracteristica_form = ""
    topico_form = ""
    if str(request.method) == 'POST':
        if len(request.POST) > 2:

            id_categoria = request.POST.get('categoria')
            form = EditarProduto(request.POST, instance=produto)
            if form.is_valid():

                nome = form.cleaned_data['nome']
                preco = form.cleaned_data['preco']
                descricao = form.cleaned_data['descricao']
                quantidade = form.cleaned_data['quantidade']
                caracteristica = form.cleaned_data['caracteristica']
                categoria = buscar_categoria(id_categoria)
                subcategoria = request.POST.get('subcategoria')
                topico = form.cleaned_data['topico']

                topico_form = topico
                caracteristica_form = caracteristica
                # vitrine = Vitrine.objects.filter(vendedor=usuario_logado, status=True).first()

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
                    caracteristica_bd = Caracteristica.objects.get(descricao=caracteristica, topico=topico,
                                                                   produto=produto)
                except Caracteristica.DoesNotExist:
                    caracteristica_produto_antigo = Caracteristica.objects.filter(status=True, produto=produto).first()
                    caracteristica_produto_antigo.status = False
                    caracteristica_produto_antigo.save()

                    caracteristica_bd = Caracteristica.objects.create(descricao=caracteristica, topico=topico,
                                                                      produto=produto)

                if not verificar_subcategoria_vazia:
                    subcategoria_bd.save()

                produto.nome = nome
                produto.preco = preco
                produto.quantidade = quantidade
                produto.descricao = descricao
                produto.categoria = categoria_bd

                categoria_bd.save()
                caracteristica_bd.save()
                produto.save()
                messages.success(request, 'Produto editado com sucesso!')
                return redirect('vitrines:minha_vitrine')

            else:
                messages.error(request, 'Erro ao enviar formulário!')

    dict_categorias = retorna_categorias()
    subcategoria = SubCategoria.objects.filter(status=True, categoria=produto.categoria).first()
    caracteristica = Caracteristica.objects.filter(status=True, produto=produto).first()
    form = EditarProduto(instance=produto)

    context = {
        'form': form,
        'usuario': usuario_logado,
        'categorias': dict_categorias,
        'subcategoria_produto': subcategoria,
        'categoria_produto': produto.categoria,
        'editar': 'editar',
        'produto_id': produto.id
    }

    return render(request, 'produtos/produto_editar.html', context)


@login_required(login_url='/usuarios/login')
def deletar_produto(request):
    if len(request.POST) == 2:
        produto = get_object_or_404(Produto, pk=request.POST.get('id'))
        recuperar_id_deletar_produto['produto'] = produto
        produto.status = False
        produto.save()

    if not recuperar_id_deletar_produto['produto'].status:
        messages.success(request, 'Produto deletado com sucesso!')

    return redirect('vitrines:minha_vitrine')

def adicionar_caracteristicas_produto(formulario, novo_produto):

    total_caracteristicas = 0
    for caracteristica in formulario:
        if 'titulo_caracteristica' in caracteristica:
            # verifica qual posição da tabela de características
            total_caracteristicas += 1

            titulo = 'titulo_caracteristica-' + str(total_caracteristicas)
            nome = 'nome_caracteristica-' + str(total_caracteristicas)
            descricao = 'descricao_caracteristica-' + str(total_caracteristicas)

            topico = formulario[titulo]
            nova_caracteristica = Caracteristica.objects.create(
                produto=novo_produto,
                topico=topico
            )
            nova_caracteristica.save()

            # pego a lista dos nomes da lista de atributos na tabela
            nomes = formulario.getlist(nome)
            # pego a lista de descriçoes da lista de atributos na tabela
            descricoes = formulario.getlist(descricao)

            index = 0
            while index < len(nomes):

                novo_atributo = Atributo.objects.create(
                    nome = nomes[index],
                    descricao = descricoes[index],
                    caracteristica = nova_caracteristica
                )
                novo_atributo.save()
                index += 1

def retornar_produto():
    if recuperar_id_editar_produto:
        produto = get_object_or_404(Produto, pk=recuperar_id_editar_produto['id'])
        return produto
