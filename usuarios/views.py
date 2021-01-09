from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView
)

from django.shortcuts import render
from django.views.generic import CreateView
from .forms import (
    CustomUsuarioCreationForm,
    UsuarioLoginForm, ResetarSenhaForm

)
from .models import (
    CustomUsuario,
    Cidade,
    Estado,
    Telefone, Endereco
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class SignUp(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('usuarios:cadastrousuario')
    form_class = CustomUsuarioCreationForm
    template_name = 'cadastros/usuario_cadastro.html'
    success_message = 'Cadastro realizado com sucesso'


class LoginCustomizado(LoginView, SuccessMessageMixin):
    authentication_form = UsuarioLoginForm
    template_name = 'registration/login.html'
    success_message = 'Login realizado com sucesso'


class ResetarSenha(PasswordResetView, SuccessMessageMixin):
    success_url = reverse_lazy('usuarios:sucessoresetarsenha')
    form_class = ResetarSenhaForm
    template_name = 'registration/password_reset_form.html'
    success_message = 'Redefinição de senha enviada com sucesso!'


class MensagemResetarSenhaEmail(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


# AJAX

def carregar_cidades(request):
    estado_id = request.GET.get('estado')
    cidades = Cidade.objects.filter(estado_id=estado_id).all()
    return render(request, 'cadastros/cidade_dropdown_list_options.html', {'cidades': cidades})
