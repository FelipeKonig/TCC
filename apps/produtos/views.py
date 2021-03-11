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

recuperar_id_deletar_produto = {}

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
                subcategoria = buscar_subcategoria_bd(categoria, request.POST.get('subcategoria'))

                novo_produto.subCategoria = subcategoria
                novo_produto.save()

            adicionar_caracteristicas_produto(request.POST, novo_produto)

            imagens_produto = request.FILES.getlist('foto')

            adicionar_imagens_produto(imagens_produto, novo_produto)

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

def visualizar_produto(request):

    produto = Produto.objects.get(pk=request.POST.get('campoIDProduto'))
    vitrine = Vitrine.objects.get(vendedor=produto.vitrine.vendedor)
    avaliacao = Avaliacao.objects.filter(produto=produto, vitrine=vitrine).first()
    imagens_produto = ImagemProduto.objects.filter(produto=produto, status=True)
    lista_caracteristicas = Caracteristica.objects.filter(produto=produto, status=True)
    lista_atributos = Atributo.objects.filter(caracteristica__in=lista_caracteristicas)

    vendedor = False
    if vitrine.vendedor == request.user:
        vendedor = True

    rating = list()
    nota = 1
    if avaliacao != None:
        while nota <= avaliacao.nota:
            rating.append(nota)
            nota += 1
            
    contexto = {
        'nota': rating,
        'produto': produto,
        'vitrine': vitrine,
        'vendedor': vendedor,
        'avaliacao': avaliacao,
        'imagens_produto': imagens_produto,
        'primeira_imagem': imagens_produto[0],
        'lista_atributos': lista_atributos,
        'lista_caracteristicas': lista_caracteristicas
    }

    return render(request, 'produtos/produto-visualizar.html', contexto)

@login_required(login_url='/usuarios/login')
def editar_produto(request):

    usuario_logado = CustomUsuario.objects.get(email=request.user)
    produto = Produto.objects.get(pk=request.POST.get('campoIDProduto'))

    if str(request.method) == 'POST':
        if len(request.POST) > 2:

            form = EditarProduto(request.POST, instance=produto)
            if form.is_valid():
                nome_categoria = request.POST.get('categoria').split('|')[0]
                vitrine = Vitrine.objects.filter(vendedor=usuario_logado, status=True).first()

                nome = form.cleaned_data['nome']
                preco = form.cleaned_data['preco']
                descricao = form.cleaned_data['descricao']
                quantidade = form.cleaned_data['quantidade']
                categoria = buscar_categoria_bd(nome_categoria)

                produto.nome = nome
                produto.preco = preco
                produto.quantidade = quantidade
                produto.descricao = descricao
                produto.categoria = categoria

                if produto.subCategoria != None:
                    if request.POST.get('subcategoria') != None:
                        subcategoria = buscar_subcategoria_bd(categoria, request.POST.get('subcategoria'))
                        produto.subCategoria = subcategoria
                    else:
                        produto.subCategoria = None
                else:
                    if request.POST.get('subcategoria') != None:
                        subcategoria = buscar_subcategoria_bd(categoria, request.POST.get('subcategoria'))
                        produto.subCategoria = subcategoria

                produto.save()

                lista_caracteristicas = Caracteristica.objects.filter(produto=produto, status=True)

                if len(lista_caracteristicas) > 0:
                    editar_caracteristicas_produto(request.POST,lista_caracteristicas, produto)

                adicionar_caracteristicas_produto(request.POST, produto)

                imagens_produto = request.FILES.getlist('foto')
                adicionar_imagens_produto(imagens_produto, produto)

                messages.success(request, 'Produto editado com sucesso!')

            else:
                messages.error(request, 'Erro ao enviar formulário!')

            return redirect('vitrines:minha_vitrine')

    lista_caracteristicas = Caracteristica.objects.filter(produto=produto, status=True)
    lista_atributos = Atributo.objects.filter(caracteristica__in=lista_caracteristicas)

    imagens_produto = ImagemProduto.objects.filter(produto=produto, status=True)
    range = 5 - len(imagens_produto)

    # definindo a quantidade de imagens disponiveis para adicionar ao produto
    # ironicamente é bem chato de fazer uma contagem de tamanho de lista no template
    lista_imagens = []
    i=1
    while i <= range:
        lista_imagens.append(i)
        i+=1

    dict_categorias = retorna_categorias()
    form = EditarProduto(instance=produto)

    context = {
        'form': form,
        'usuario': usuario_logado,
        'categorias': dict_categorias,
        'lista_caracteristicas': lista_caracteristicas,
        'lista_atributos': lista_atributos,
        'imagens': imagens_produto,
        'range': lista_imagens,
        'produto': produto,
        'editar': 'editar'
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

def adicionar_imagens_produto(imagens_produto, produto):

    index = 0
    while index < len(imagens_produto):

        nova_imagem = ImagemProduto.objects.create(
            imagem = imagens_produto[index],
            produto = produto
        )
        nova_imagem.save()
        index += 1

def editar_caracteristicas_produto(formulario, lista_caracteristicas, produto):

    lista_atributos = Atributo.objects.filter(caracteristica__in=lista_caracteristicas)

    index_caract = 0
    while index_caract < len(lista_caracteristicas):
        caracteristica = lista_caracteristicas[index_caract]

        titulo = 'titulo-caracteristica-' + str(caracteristica.pk)
        nome = 'nome-caracteristica-' + str(caracteristica.pk)
        descricao = 'descricao-caracteristica-' + str(caracteristica.pk)

        topico = formulario[titulo]

        if caracteristica.topico != topico:
            Caracteristica.objects.filter(pk=caracteristica.pk).update(topico=topico)

        # pego a lista dos nomes da lista de atributos na tabela
        nomes = formulario.getlist(nome)
        # pego a lista de descriçoes da lista de atributos na tabela
        descricoes = formulario.getlist(descricao)

        # fazendo uma consulta no banco deletando todos os objetos da respectiva tabela de caracteristica
        # que foram alterados ou deletados
        atributos_alterados = Atributo.objects.filter(caracteristica_id=caracteristica.pk).exclude(
            nome__in=nomes,
            descricao__in=descricoes
        ).delete()

        index_atributo = 0
        while index_atributo < len(nomes):

            # [0] para não dar erro de multiplos objetos quando houver dois novos atributos com mesmo nome
            # e descrição, evita o erro e também duplicação de objetos
            atributo = Atributo.objects.get_or_create(
                nome = nomes[index_atributo],
                descricao = descricoes[index_atributo],
                caracteristica = caracteristica
            )[0]

            index_atributo += 1
        index_caract += 1

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
