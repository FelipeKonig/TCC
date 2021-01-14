from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    ListView
)
from .forms import CadastroEmpresa

from .models import Empresa
from apps.usuarios.models import CustomUsuario


class CriarEmpresa(CreateView):

    def get(self, request, *args, **kwargs):
        form = super().get_form(CadastroEmpresa)
        empresa = self.request.user.empresa

        query_set = ''
        if empresa is None:
            query_set = Empresa.objects.none()
        else:
            query_set = Empresa.objects.filter(cnpj=empresa.cnpj, status=True)

        context = {
            'form': form,
            'empresa': query_set
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
                    cnpj_cortado_digitos_finais = str(cnpj).split('-')
                    cnpj_cortado_digitos_iniciais = cnpj_cortado_digitos_finais[0].split('.')
                    cnpj_cortado_digitos_meio = ''
                    cnpj_sem_formatacao = ''
                    tamanho_lista_digito_inicial = len(cnpj_cortado_digitos_iniciais)

                    for i in range(0, tamanho_lista_digito_inicial, 1):
                        if i != 2:
                            cnpj_sem_formatacao = cnpj_sem_formatacao + cnpj_cortado_digitos_iniciais[i]
                        elif i == 2:
                            cnpj_cortado_digitos_meio = cnpj_cortado_digitos_iniciais[i].split('/')

                    tamanho_lista_digito_meio = len(cnpj_cortado_digitos_meio)

                    for i in range(0, tamanho_lista_digito_meio, 1):
                        cnpj_sem_formatacao += cnpj_cortado_digitos_meio[i]

                    cnpj_sem_formatacao += cnpj_cortado_digitos_finais[1]
                    cnpj = cnpj_sem_formatacao

            print(form.cleaned_data)
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


class ListarEmpresas(ListView):
    model = Empresa
    template_name = 'empresas/empresa_listar.html'
    # queryset = Empresa.objects.all()
    context_object_name = 'empresas'

    def get_queryset(self):
        empresa = self.request.user.empresa
        query_set = ''
        if empresa is None:
            query_set = Empresa.objects.none()
        else:
            query_set = Empresa.objects.filter(cnpj=empresa.cnpj, status=True)

        return query_set


def deletar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, id=pk)
    empresa.status = False
    empresa.save()
    messages.success(request, 'Empresa deletada com sucesso!')
    return redirect('empresas:listar_empresas')
