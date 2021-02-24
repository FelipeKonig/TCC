from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    UpdateView,
)
from ..forms import CadastroEmpresa, EditarEmpresaForm

from ..models import Empresa
from ...usuarios.models import Telefone, Endereco
from apps.usuarios.models import CustomUsuario
from apps.usuarios.views.endereco import buscar_estados_api

recuperar_id_empresa_editar = {}
recuperar_id_empresa_deletar = {}

from validate_docbr import CNPJ


# Metodo para retornar se existe uma empresa ativa ou não
def consulta_empresa(empresa):
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

@login_required(login_url='/usuarios/login')
def empresa_perfil(request):

    if request.method == 'POST' and request.FILES['foto']:
        empresa = Empresa.objects.get(pk=request.user.empresa.pk)
        nova_logo = request.FILES['foto']
        fs = FileSystemStorage()
        uploaded_file_url = fs.url(nova_logo)
        empresa.logo = nova_logo
        empresa.save()

    if request.user.empresa != None:
        empresa = Empresa.objects.get(pk=request.user.empresa.pk)
    else:
        empresa = None
    enderecos = Endereco.objects.filter(usuario=request.user, empresa=empresa, status=True)
    telefones = Telefone.objects.filter(usuario=request.user, empresa=empresa, status=True)
    usuario_logado = CustomUsuario.objects.get(email=request.user)

    contexto = {
        'empresa': empresa,
        'enderecos': enderecos,
        'telefones': telefones,
        'usuario': usuario_logado
    }
    return render(request,'empresas/empresa_perfil.html', contexto)


@login_required(login_url='/usuarios/login')
def deletar_empresa(request):
    if len(request.POST) == 2:
        empresa = get_object_or_404(Empresa, pk=request.POST.get('id'))
        recuperar_id_empresa_deletar['empresa'] = empresa
        empresa.status = False
        empresa.save()
    if not recuperar_id_empresa_deletar['empresa'].status:
        messages.success(request, 'Empresa deletada com sucesso!')

    return redirect('')


class CriarEmpresa(LoginRequiredMixin, CreateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        form = super().get_form(CadastroEmpresa)
        empresa = self.request.user.empresa
        query_set = consulta_empresa(empresa)
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        enderecos = Endereco.objects.filter(usuario=request.user, status=True)

        estados = buscar_estados_api()
        context = {
            'form': form,
            'empresa': query_set,
            'enderecos': enderecos,
            'estados': estados,
            'usuario': usuario_logado
        }
        return render(request, 'empresas/empresa_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(CadastroEmpresa)

        if form.is_valid():
            razaoSocial = form.cleaned_data['razaoSocial']
            nomeFantasia = form.cleaned_data['fantasia']
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
                                             fantasia=nomeFantasia, logo=logo)

            if request.POST['inscricaoEstadual']:
                inscricaoEstadual = form.cleaned_data['inscricaoEstadual']
                empresa.inscricaoEstadual=inscricaoEstadual
            if request.POST['inscricaoMunicipal']:
                inscricaoMunicipal = form.cleaned_data['inscricaoMunicipal']
                empresa.inscricaoMunicipal=inscricaoMunicipal

            usuario = self.request.user
            usuario_bd = CustomUsuario.objects.get(email=usuario.email)
            usuario_bd.empresa = empresa
            usuario_bd.save()

            if request.POST['numero_telefone'] != '':
                telefones = Telefone.objects.filter(usuario=usuario_bd, empresa=usuario_bd.empresa, status=True)
                verificar_telefone(request.POST, usuario_bd, telefones)

            return redirect('empresas:empresa_perfil')

        else:
            messages.error(request, 'Erro ao enviar o formulário !')

        context = {
            'form': form
        }

        return render(request, 'empresas/empresa_cadastro.html', context)

@login_required(login_url='/usuarios/login')
def editar_empresa(request):
    usuario = CustomUsuario.objects.get(email=request.user)
    empresa = usuario.empresa
    form = EditarEmpresaForm(request.POST or None)

    if str(request.method) == 'POST':
        if len(request.POST) > 2:
            form = EditarEmpresaForm(request.POST, instance=empresa)
            cnpj = CNPJ()

            aux_cnpj = request.POST.get('cnpj')
            resultado_validacao = cnpj.validate(aux_cnpj)

            if not resultado_validacao:
                messages.error(request, 'CNPJ inválido')

            if form.is_valid():
                razaoSocial = form.cleaned_data['razaoSocial']
                nomeFantasia = form.cleaned_data['fantasia']
                inscricaoEstadual = form.cleaned_data['inscricaoEstadual']
                inscricaoMunicipal = form.cleaned_data['inscricaoMunicipal']
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
                empresa.cnpj = cnpj

                if request.POST['numero_telefone'] != '':
                    telefones = Telefone.objects.filter(empresa=usuario.empresa, status=True)
                    verificar_telefone(request.POST, usuario, telefones)

                empresa.save()
                messages.success(request, 'Empresa editada com sucesso!')
                return redirect('empresas:empresa_perfil')

    estados = buscar_estados_api()
    telefones = Telefone.objects.filter(empresa=usuario.empresa, status=True)
    form = EditarEmpresaForm(instance=empresa)

    context = {
        'usuario': usuario,
        'form': form,
        'estados': estados,
        'telefones': telefones,
        'editar': 'editar'
    }

    return render(request, 'empresas/empresa_cadastro.html', context)

def verificar_telefone(formulario, usuario, telefones):
    # se o usuario não ter deletado o único número dele
    if len(telefones) > 0:
        if telefones[0].tipo != formulario['tipo_telefone'] or telefones[0].numero != formulario['numero_telefone']:

            atualizar_telefone = Telefone.objects.get(
                usuario=usuario,
                empresa=usuario.empresa,
                tipo=telefones[0].tipo,
                numero=telefones[0].numero
            )
            atualizar_telefone.numero = formulario['numero_telefone']
            atualizar_telefone.tipo = formulario['tipo_telefone']

            atualizar_telefone.save()
    else:
        telefone = Telefone.objects.create(
            usuario=usuario,
            empresa=usuario.empresa,
            tipo=formulario['tipo_telefone'],
            numero=formulario['numero_telefone']
        )

    if formulario['numero_telefone2'] != '':
        if len(telefones) > 1:
            if telefones[1].tipo != formulario['tipo_telefone2'] or telefones[1].numero != formulario['numero_telefone2']:

                atualizar_telefone = Telefone.objects.get(
                    usuario=usuario,
                    empresa=usuario.empresa,
                    tipo=telefones[1].tipo,
                    numero=telefones[1].numero
                )
                atualizar_telefone.numero = formulario['numero_telefone2']
                atualizar_telefone.tipo = formulario['tipo_telefone2']
                atualizar_telefone.save()
        else:
            telefone = Telefone.objects.create(
                usuario=usuario,
                empresa=usuario.empresa,
                tipo=formulario['tipo_telefone2'],
                numero=formulario['numero_telefone2']
            )
