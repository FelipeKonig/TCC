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

    contexto = {
        'usuario': usuario
    }
    return render(request, 'ecommerce/pagina-index.html', contexto)
