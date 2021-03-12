import logging

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .models import *
from apps.produtos.models import *

logger = logging.getLogger(__name__)

# Create your views here.
def visualizar_carrinho(request):

    pedidos = Pedido.objects.filter(cliente=request.user, status=False)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos, status=False)

    pedidos_vazio = False
    if len(pedidos_produtos) == 0:
        pedidos_vazio = True

    quantidade_total = 0
    preco_total = 0
    for pedido in pedidos_produtos:
        quantidade_total += pedido.quantidade
        preco_total += float(float(pedido.preco) * float(pedido.quantidade))

    preco_total = float("{:.2f}".format(preco_total))

    imagem_produto = list()
    lista_pedidos = list()

    index = 0
    while index < len(pedidos_produtos):
        pedido = pedidos_produtos[index]
        lista_pedidos.append('{}-{}-{}'.format(pedido.produto.nome,pedido.pedido.pk,pedido.produto.pk))

        imagem = ImagemProduto.objects.filter(produto=pedido.produto).first()
        imagem_produto.append(imagem)
        index += 1

    contexto = {
        'pedidos_vazio': pedidos_vazio,
        'pedidos': pedidos,
        'preco_total': preco_total,
        'quantidade_total': quantidade_total,
        'lista_pedidos': lista_pedidos,
        'imagem_produto': imagem_produto,
        'pedidos_produtos': pedidos_produtos
    }

    return render(request, 'carrinhos/pagina-carrinho.html', contexto)

# AJAX
def alterar_quantidade_produto_pedido(request):

    pedido_id = request.GET.get('produto').split('_')
    quantidade = request.GET.get('quantidade')
    pedido_produto = Pedido_Produto.objects.filter(pedido__pk=pedido_id[2], produto__pk=pedido_id[3], status=False).first()
    pedido_produto.quantidade=quantidade
    preco = float(pedido_produto.produto.preco)

    preco_total = float(preco * float(quantidade))
    pedido_produto.precoTotal = preco_total

    pedido_produto.save()

    pedidos = Pedido.objects.filter(cliente=request.user)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos)

    quantidade_total = 0
    preco_total = 0

    for pedido in pedidos_produtos:
        quantidade_total += pedido.quantidade
        preco_total += float(float(pedido.preco) * float(pedido.quantidade))

    preco_total = float("{:.2f}".format(preco_total))

    contexto = {
        'produto': model_to_dict(pedido_produto),
        'preco_total': preco_total,
        'quantidade_total': quantidade_total
    }

    if request.is_ajax():
        return JsonResponse(contexto)

def remover_produto_pedido(request):

    produto_pedido = request.GET.get('produto').split('_')

    produto = Pedido_Produto.objects.filter(pk=produto_pedido[1], produto__nome=produto_pedido[0], status=False).delete()

    pedidos = Pedido.objects.filter(cliente=request.user, status=False)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos, status=False)

    pedidos_vazio = False
    if len(pedidos_produtos) == 0:
        pedidos_vazio = True

    contexto = {
        'pedidos_vazio': pedidos_vazio
    }

    if request.is_ajax():
        return JsonResponse(contexto)
