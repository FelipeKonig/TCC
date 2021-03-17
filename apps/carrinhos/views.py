import logging

from datetime import date
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.produtos.models import *
from apps.usuarios.models import *

logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url='/usuarios/login')
def visualizar_carrinho(request):

    pedidos = Pedido.objects.filter(cliente=request.user, statusReservado=False)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos, statusReservado=False, statusFinalizado=False)

    pedidos_vazio = False
    if len(pedidos) == 0:
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
        'usuario': request.user,
        'pedidos_vazio': pedidos_vazio,
        'pedidos': pedidos,
        'preco_total': preco_total,
        'quantidade_total': quantidade_total,
        'lista_pedidos': lista_pedidos,
        'imagem_produto': imagem_produto,
        'pedidos_produtos': pedidos_produtos
    }

    return render(request, 'carrinhos/pagina-carrinho.html', contexto)

@login_required(login_url='/usuarios/login')
def adicionar_produto_carrinho(request):

    produto = get_object_or_404(Produto, pk=request.POST['produto'])

    pedido = Pedido.objects.get_or_create(cliente=request.user, statusReservado=False)

    quantidade = request.POST['quant_produto']
    preco = float(produto.preco)

    preco_total = float(preco * float(quantidade))

    try:
        pedido_produto = Pedido_Produto.objects.get(
            pedido=pedido[0],
            vendedor=produto.vitrine,
            produto=produto,
            statusReservado=False,
            statusFinalizado=False
        )

        pedido_produto.quantidade=quantidade
        pedido_produto.preco=produto.preco
        pedido_produto.precoTotal=preco_total
        pedido_produto.dataCriacao=date.today()

        pedido_produto.save()
    except:
        pedido_produto = Pedido_Produto.objects.create(
            pedido=pedido[0],
            vendedor=produto.vitrine,
            produto=produto,
            quantidade=quantidade,
            preco=produto.preco,
            precoTotal=preco_total,
            dataCriacao=date.today(),
            statusReservado=False,
            statusFinalizado=False
        )

    return redirect('pedidos:visualizar_carrinho')

@login_required(login_url='/usuarios/login')
def remover_produto_pedido(request):

    produto_pedido = request.GET.get('produto').split('_')

    produto = Pedido_Produto.objects.filter(
        pk=produto_pedido[1],
        produto__nome=produto_pedido[0],
        statusReservado=False,
        statusFinalizado=False
    ).delete()

    pedidos = Pedido.objects.filter(cliente=request.user, statusReservado=False)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos, statusReservado=False, statusFinalizado=False)

    pedidos_vazio = False
    if len(pedidos_produtos) == 0:
        pedidos_vazio = True

    contexto = {
        'pedidos_vazio': pedidos_vazio
    }

    if request.is_ajax():
        return JsonResponse(contexto)

# AJAX
@login_required(login_url='/usuarios/login')
def alterar_quantidade_produto_pedido(request):

    pedido_id = request.GET.get('produto').split('_')
    quantidade = request.GET.get('quantidade')
    pedido_produto = Pedido_Produto.objects.filter(
        pedido__pk=pedido_id[2],
        produto__pk=pedido_id[3],
        statusReservado=False,
        statusFinalizado=False
    ).first()

    pedido_produto.quantidade=quantidade
    preco = float(pedido_produto.produto.preco)

    preco_total = float(preco * float(quantidade))
    pedido_produto.precoTotal = preco_total

    pedido_produto.save()

    pedidos = Pedido.objects.filter(cliente=request.user, statusReservado=False)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos, statusReservado=False)

    quantidade_total = 0
    preco_total = 0

    for pedido in pedidos_produtos:
        quantidade_total += pedido.quantidade
        preco_total += float(float(pedido.preco) * float(pedido.quantidade))

    preco_total = float("{:.2f}".format(preco_total))

    contexto = {
        'usuario': request.user,
        'produto': model_to_dict(pedido_produto),
        'preco_total': preco_total,
        'quantidade_total': quantidade_total
    }

    if request.is_ajax():
        return JsonResponse(contexto)

@login_required(login_url='/usuarios/login')
def listar_pedidos(request):

    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, cliente=request.user, statusReservado=False)
        pedidos_produtos = Pedido_Produto.objects.filter(pedido=pedido, statusReservado = False).update(statusReservado = True)

        pedido.statusReservado = True
        pedido.save()

    pedidos = Pedido.objects.filter(cliente=request.user, statusReservado=True)
    pedidos_produtos = Pedido_Produto.objects.filter(pedido__in=pedidos, statusReservado = True)

    pedidos_vazio = False
    if len(pedidos) == 0 or len(pedidos_produtos) == 0:
        pedidos_vazio = True

    quantidade_pedidos_total = 0
    pedidos_entregues_total = 0
    for pedido in pedidos_produtos:
        quantidade_pedidos_total += 1
        if pedido.statusFinalizado:
            pedidos_entregues_total += 1

    imagem_produto = list()

    index = 0
    while index < len(pedidos_produtos):
        pedido = pedidos_produtos[index]
        imagem = ImagemProduto.objects.filter(produto=pedido.produto).first()

        repetida = False
        for imagem2 in imagem_produto:
            if imagem == imagem2:
                repetida = True

        if not repetida:
            imagem_produto.append(imagem)

        index += 1

    contexto = {
        'pedidos': pedidos,
        'usuario': request.user,
        'pedidos_vazio': pedidos_vazio,
        'imagem_produto': imagem_produto,
        'pedidos_produtos': pedidos_produtos,
        'pedidos_entregues_total': pedidos_entregues_total,
        'quantidade_pedidos_total': quantidade_pedidos_total
    }

    return render(request, 'carrinhos/listar_pedidos.html', contexto)

@login_required(login_url='/usuarios/login')
def visualizar_produto_pedido(request, pk_pedido, pk_pedido_produto, pk_produto, nome_produto):

    pedido_produto = get_object_or_404(Pedido_Produto, pedido_id=pk_pedido, pk=pk_pedido_produto, produto_id=pk_produto)

    pedido_status = False
    if pedido_produto.statusReservado:
        pedido_status = True

    produto = pedido_produto.produto
    vitrine = pedido_produto.vendedor
    quantidade = pedido_produto.quantidade

    if vitrine.empresa == None:
        endereco = Endereco.objects.filter(usuario=vitrine.vendedor, padrao=True, status=True).first()
        enderecos = Endereco.objects.filter(usuario=vitrine.vendedor, padrao=False,empresa=None, status=True)

        telefone_padrao = Telefone.objects.filter(usuario=vitrine.vendedor, empresa=None, padrao=True, status=True).first()
        telefone_alternativo = Telefone.objects.filter(usuario=vitrine.vendedor, empresa=None, padrao=False, status=True).first()
    else:
        endereco = Endereco.objects.filter(empresa=vitrine.empresa, padrao=True, status=True).first()
        enderecos = Endereco.objects.filter(usuario=vitrine.vendedor, padrao=False, status=True)

        telefone_padrao = Telefone.objects.filter(empresa=vitrine.empresa, padrao=True, status=True).first()
        telefone_alternativo = Telefone.objects.filter(empresa=vitrine.empresa, padrao=False, status=True).first()

    encomendas = Pedido_Produto.objects.filter(produto=produto, statusFinalizado=True).count()
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
        'usuario': request.user,
        'pedido': pedido_produto,
        'nota': rating,
        'produto': produto,
        'vitrine': vitrine,
        'endereco':endereco,
        'vendedor': vendedor,
        'avaliacao': avaliacao,
        'enderecos': enderecos,
        'encomendas': encomendas,
        'telefone_padrao': telefone_padrao,
        'imagens_produto': imagens_produto,
        'lista_atributos': lista_atributos,
        'primeira_imagem': imagens_produto[0],
        'telefone_alternativo':telefone_alternativo,
        'lista_caracteristicas': lista_caracteristicas
    }

    return render(request, 'produtos/produto-visualizar.html', contexto)
