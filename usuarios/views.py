from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView
)

from django.shortcuts import render
from django.views.generic import CreateView
from .forms import (
    CustomUsuarioCreationForm,
    UsuarioLoginForm,
    EmailTokenSenhaForm,
    ResetarSenhaForm,
    AlterarSenhaForm

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


# ---------------- Redefinição de senha ----------------
class EmailTokenSenha(PasswordResetView):
    success_url = reverse_lazy('usuarios:sucessoresetarsenha')
    form_class = EmailTokenSenhaForm
    template_name = 'registration/password_reset_form.html'


class MensagemResetarSenhaEmail(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class ResetarSenha(PasswordResetConfirmView):
    success_url = reverse_lazy('usuarios:redifinicaocompleta')
    form_class = ResetarSenhaForm
    template_name = 'registration/password_reset_confirm.html'


class ResetarSenhaMensagemCompleta(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# ---------- Alteração de senha
class AlteracaoSenha(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    login_url = '/usuarios/login'
    form_class = AlterarSenhaForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('usuarios:alterarsenha')
    success_message = 'Senha alterada com sucesso'

# AJAX ----
# Esta função pode ser apagada  ! -----

def carregar_cidades(request):
    estado_id = request.GET.get('estado')
    cidades = Cidade.objects.filter(estado_id=estado_id).all()
    return render(request, 'cadastros/cidade_dropdown_list_options.html', {'cidades': cidades})
