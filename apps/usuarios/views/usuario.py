import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView
)

from ..forms import (
    CustomUsuarioCreationForm,
    UsuarioLoginForm,
    EmailTokenSenhaForm,
    ResetarSenhaForm,
    AlterarSenhaForm,
    CadastroPerfilUsuario
)

from ..models import (
    CustomUsuario,
    Telefone, Endereco,
    adicionar_imagem_perfil
)

logger = logging.getLogger(__name__)

@login_required(login_url='/usuarios/login')
def perfil_principal(request):

    enderecos = Endereco.objects.filter(usuario=request.user, status=True)
    telefones = Telefone.objects.filter(usuario=request.user, status=True)
    usuario_logado = CustomUsuario.objects.get(email=request.user)

    if request.method == 'POST' and request.FILES['foto']:
        usuario = CustomUsuario.objects.get(email=request.user)
        nova_foto = request.FILES['foto']
        fs = FileSystemStorage()
        uploaded_file_url = fs.url(nova_foto)
        usuario.foto = nova_foto
        usuario.save()

    context = {
        'enderecos': enderecos,
        'telefones': telefones,
        'usuario':usuario_logado
    }
    return render(request, 'usuarios/dados_perfil_usuario.html', context)

@login_required(login_url='/usuarios/login')
def perfil_configuracao(request):

    if request.method == 'POST':

        telefones = Telefone.objects.filter(usuario=request.user, status=True)
        usuario = request.user
        usuario.first_name = request.POST['nome']
        usuario.last_name = request.POST['sobrenome']
        usuario.email = request.POST['email']

        if request.POST['numero_telefone'] != '':
            # se o usuario não ter deletado o único número dele
            if len(telefones) > 0:
                if telefones[0].tipo != request.POST['tipo_telefone'] or telefones[0].numero != request.POST['numero_telefone']:

                    atualizar_telefone = Telefone.objects.get(
                        usuario=usuario,
                        tipo=telefones[0].tipo,
                        numero=telefones[0].numero
                    )
                    atualizar_telefone.numero = request.POST['numero_telefone']
                    atualizar_telefone.tipo = request.POST['tipo_telefone']
                    atualizar_telefone.save()
            else:
                telefone = Telefone.objects.create(
                usuario=usuario,
                tipo=request.POST['tipo_telefone'],
                numero=request.POST['numero_telefone']
                )
                atualizar_telefone.save()

            if request.POST['numero_telefone2'] != '':
                if len(telefones) > 1:
                    if telefones[1].tipo != request.POST['tipo_telefone2'] or telefones[1].numero != request.POST['numero_telefone2']:

                        atualizar_telefone = Telefone.objects.get(
                            usuario=usuario,
                            tipo=telefones[1].tipo,
                            numero=telefones[1].numero
                        )
                        atualizar_telefone.numero = request.POST['numero_telefone2']
                        atualizar_telefone.tipo = request.POST['tipo_telefone2']
                        atualizar_telefone.save()
                else:
                    telefone = Telefone.objects.create(
                        usuario=usuario,
                        tipo=request.POST['tipo_telefone2'],
                        numero=request.POST['numero_telefone2']
                    )
                    messages.success(request, 'Perfil atualizado!')
                    atualizar_telefone.save()

        usuario.save()
    # atualizando os telefones
    telefones = Telefone.objects.filter(usuario=request.user, status=True)

    return render(request, 'usuarios/perfil-configuracao.html', {'telefones':telefones})

# ---------------- Cadastro usuário ----------------
class CriarPerfilUsuario(LoginRequiredMixin, CreateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        form = super().get_form(CadastroPerfilUsuario)
        context = {
            'form': form,
            'usuario': usuario_logado
        }
        return render(request, 'usuarios/cadastros/usuario_perfil_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(CadastroPerfilUsuario)
        empresa_selecionado = ""

        if form.is_valid():
            usuario_logado = CustomUsuario.objects.get(email=request.user)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            data_nascimento = form.cleaned_data['data_nascimento']
            cpf = form.cleaned_data['cpf']
            empresa_selecionado = form.cleaned_data['empresa_selecionar']
            numeroTelefone = form.cleaned_data['numeroTelefone']
            foto = form.cleaned_data['foto']
            tipoTelefone = form.cleaned_data['telefone_selecionar']

            if cpf:
                if len(cpf) == 14:
                    cpf_cortado_digitos_finais = str(cpf).split('-')
                    cpf_cortado_digitos_iniciais = cpf_cortado_digitos_finais[0].split('.')
                    cpf_sem_formatacao_mascara = ''

                    for numero in cpf_cortado_digitos_iniciais:
                        cpf_sem_formatacao_mascara += numero

                    cpf_sem_formatacao_mascara += cpf_cortado_digitos_finais[1]

            telefone = Telefone.objects.create(tipo=tipoTelefone, numero=numeroTelefone, usuario=usuario_logado)
            usuario_logado.first_name = first_name
            usuario_logado.last_name = last_name
            usuario_logado.data_nascimento = data_nascimento
            usuario_logado.foto = foto
            usuario_logado.telefone = telefone
            usuario_logado.status = True

            if len(cpf) == 14:
                usuario_logado.cpf = cpf_sem_formatacao_mascara
            else:
                usuario_logado.cpf = cpf

            usuario_logado.save()
            messages.success(request, 'Perfil cadastrado com sucesso!')
            form = CadastroPerfilUsuario()

        context = {
            'form': form,
            'empresaSelecionada': empresa_selecionado,
        }

        return render(request, 'usuarios/cadastros/usuario_perfil_cadastro.html', context)


class SignUp(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('usuarios:cadastrousuario')
    form_class = CustomUsuarioCreationForm
    template_name = 'usuarios/cadastros/usuario_cadastro.html'
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


# ---------------- Alteração de senha ----------------
class AlteracaoSenha(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    login_url = '/usuarios/login'
    form_class = AlterarSenhaForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('usuarios:alterarsenha')
    success_message = 'Senha alterada com sucesso'

# class ListarUsuario(LoginRequiredMixin, ListView):
#   login_url = 'usuarios/login'
#  model = CustomUsuario
# template_name = 'usuarios/perfil-principal.html'
# context_object_name = 'enderecos'

# def get_queryset(self):
#   query_set = Endereco.objects.filter(usuario=self.request.user, status=True)
#  return query_set
