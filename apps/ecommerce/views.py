import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.usuarios.models import CustomUsuario
from apps.empresas.models import Empresa
from apps.produtos.models import *

# Create your views here.
logger = logging.getLogger(__name__)

def home_page(request):

    usuario = CustomUsuario.objects.filter(email=request.user).first()
    produtos = Produto.objects.order_by('numero_acessos')[:16]
    produtos = list(produtos)
    avaliacoes = Avaliacao.objects.filter(produto__in=produtos).order_by('-nota')
    imagens_produto = ImagemProduto.objects.filter(produto__in=produtos)

    contexto = {
        'usuario': usuario,
        'avaliacoes_produto': avaliacoes,
        'imagens_produto': imagens_produto
    }
    return render(request, 'ecommerce/pagina-index.html', contexto)
