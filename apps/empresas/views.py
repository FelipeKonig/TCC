from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)
from .forms import CadastroEmpresa

from .models import Empresa
from ..usuarios.models import Telefone, Endereco
from apps.usuarios.models import CustomUsuario


# Metodo para retornar se existe uma empresa ativa ou não
def consulta_Empresa(empresa):
    if empresa is None:
        query_set = Empresa.objects.none()
    else:
        query_set = Empresa.objects.filter(cnpj=empresa.cnpj, status=True)
    return query_set


def cnpj_sem_formatacao(cnpj):
    cnpj_cortado_digitos_finais = str(cnpj).split('-')
    cnpj_cortado_digitos_iniciais = cnpj_cortado_digitos_finais[0].split('.')
    cnpj_cortado_digitos_meio = ''
    aux_cnpj_sem_formatacao = ''
    tamanho_lista_digito_inicial = len(cnpj_cortado_digitos_iniciais)

    for i in range(0, tamanho_lista_digito_inicial, 1):
        if i != 2:
            aux_cnpj_sem_formatacao = aux_cnpj_sem_formatacao + cnpj_cortado_digitos_iniciais[i]
        elif i == 2:
            cnpj_cortado_digitos_meio = cnpj_cortado_digitos_iniciais[i].split('/')

    tamanho_lista_digito_meio = len(cnpj_cortado_digitos_meio)

    for i in range(0, tamanho_lista_digito_meio, 1):
        aux_cnpj_sem_formatacao += cnpj_cortado_digitos_meio[i]

    aux_cnpj_sem_formatacao += cnpj_cortado_digitos_finais[1]
    return aux_cnpj_sem_formatacao


class CriarEmpresa(LoginRequiredMixin, CreateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        form = super().get_form(CadastroEmpresa)
        empresa = self.request.user.empresa
        query_set = consulta_Empresa(empresa)
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        enderecos = Endereco.objects.filter(usuario=request.user, status=True)
        telefones = Telefone.objects.filter(usuario=request.user, status=True)

        context = {
            'form': form,
            'empresa': query_set,
            'enderecos': enderecos,
            'telefones': telefones,
            'usuario': usuario_logado
        }
        return render(request, 'empresas/empresa_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(CadastroEmpresa)

        if form.is_valid():
            razaoSocial = form.cleaned_data['razaoSocial']
            nomeFantasia = form.cleaned_data['fantasia']
            inscricaoEstadual = form.cleaned_data['inscricaoEstadual']
            inscricaoMunicipal = form.cleaned_data['inscricaoMunicipal']
            logo = form.cleaned_data['logo']
            cnpj = form.cleaned_data['cnpj']

            if cnpj:
                if len(cnpj) == 18:
                    cnpj = cnpj_sem_formatacao(cnpj)
                else:
                    messages.error(request, 'CNPJ inválido')
            else:
                messages.error(request, 'CNPJ inválido')

            empresa = Empresa.objects.create(cnpj=cnpj, razaoSocial=razaoSocial,
                                             fantasia=nomeFantasia, inscricaoEstadual=inscricaoEstadual,
                                             inscricaoMunicipal=inscricaoMunicipal, logo=logo)
            usuario = self.request.user
            usuario_bd = CustomUsuario.objects.get(email=usuario.email)
            usuario_bd.empresa = empresa
            usuario_bd.save()

            #     empresa.save()
            return redirect('empresas:listar_empresas')

        else:
            messages.error(request, 'Erro ao enviar o formulário !')

        context = {
            'form': form
        }

        if messages:
            context['m'] = messages

        return render(request, 'empresas/empresa_cadastro.html', context)


class ListarEmpresa(LoginRequiredMixin, ListView):
    login_url = '/usuarios/login'
    model = Empresa
    template_name = 'empresas/empresa_listar.html'
    context_object_name = 'empresas'

    def get_queryset(self):
        empresa = self.request.user.empresa
        query_set = consulta_Empresa(empresa)
        return query_set


@login_required(login_url='/usuarios/login')
def deletar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, id=pk)
    empresa.status = False
    empresa.save()
    messages.success(request, 'Empresa deletada com sucesso!')
    return redirect('empresas:listar_empresas')


class EditarEmpresa(LoginRequiredMixin, UpdateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        empresa = get_object_or_404(Empresa, pk=self.kwargs['pk'])
        form = CadastroEmpresa(instance=empresa)

        context = {
            'form': form,
            'editar': 'editar'
        }
        return render(request, 'empresas/empresa_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        empresa = get_object_or_404(Empresa, pk=self.kwargs['pk'])
        form = self.get_form(CadastroEmpresa)

        if form.is_valid():
            razaoSocial = form.cleaned_data['razaoSocial']
            nomeFantasia = form.cleaned_data['fantasia']
            inscricaoEstadual = form.cleaned_data['inscricaoEstadual']
            inscricaoMunicipal = form.cleaned_data['inscricaoMunicipal']
            logo = form.cleaned_data['logo']
            cnpj = form.cleaned_data['cnpj']

            if cnpj:
                if len(cnpj) == 18:
                    cnpj = cnpj_sem_formatacao(cnpj)

                else:
                    messages.error(request, 'CNPJ inválido')
            else:
                messages.error(request, 'CNPJ inválido')

            empresa.razaoSocial = razaoSocial
            empresa.fantasia = nomeFantasia
            empresa.inscricaoEstadual = inscricaoEstadual
            empresa.inscricaoMunicipal = inscricaoMunicipal
            empresa.logo = logo
            empresa.cnpj = cnpj

            empresa.save()
            messages.success(request, 'Empresa editada com sucesso!')
            return redirect('empresas:listar_empresas')

        context = {
            'form': form,
            'editar': 'editar'
        }

        return render(request, 'empresas/empresa_cadastro.html', context)
