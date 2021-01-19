import logging

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView
from ..forms import (
    CustomUsuarioCreationForm,
    UsuarioLoginForm
)
from ..models import CustomUsuario, Endereco
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

logger = logging.getLogger(__name__)

class SignUpView(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('usuarios:cadastrousuario')
    form_class = CustomUsuarioCreationForm
    template_name = 'cadastros/usuario_cadastro.html'
    success_message = 'Cadastro realizado com sucesso'


class CustomLoginView(LoginView, SuccessMessageMixin):
    authentication_form = UsuarioLoginForm
    template_name = 'registration/login.html'
    success_message = 'Login realizado com sucesso'

@login_required(login_url='/usuarios/login')
def perfil_principal(request):
    enderecos = Endereco.objects.filter(usuario=request.user, status = True)
    return render(request, 'usuarios/perfil-principal.html', {'enderecos':enderecos})

@login_required(login_url='/usuarios/login')
def perfil_configuracao(request):
    return render(request, 'usuarios/perfil-configuracao.html')
