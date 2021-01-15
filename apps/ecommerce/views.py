from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging

# Create your views here.
logger = logging.getLogger(__name__)


def home_page(request):
    return render(request, 'ecommerce/pagina-index.html')
<<<<<<< HEAD:apps/ecommerce/views.py


@login_required(login_url='/usuarios/login')
def perfil_principal(request):
    return render(request, 'usuarios/dados_perfil_usuario.html')
=======
>>>>>>> dda3065af2350bb402bb1ef1d4c1773066c3986e:ecommerce/views.py
