from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Empresa
from ...usuarios.models import Telefone, Endereco
from apps.usuarios.models import CustomUsuario
from apps.usuarios.forms import EnderecoForm
from apps.usuarios.views.endereco import (
    verificar_endereco_adicionar,
    verificar_endereco_editar,
    buscar_estados_api,
    buscar_cidades_api
)

def empresa_endereco(request):

    enderecos = Endereco.objects.filter(usuario=request.user, empresa=request.user.empresa, status=True)

    return render(request, 'empresas/endereco/empresa-endereco.html', {'enderecos': enderecos})

@login_required(login_url='/usuarios/login')
def adicionar_endereco(request):

    if request.method == "POST":

        endereco = verificar_endereco_adicionar(request.POST['estado'],
            request.POST['cidade'],
            request.POST['cep'],
            request.POST['bairro'],
            request.POST['rua'],
            request.POST['numero'],
            request.POST['complemento']
        )

        if endereco != '':
            endereco.usuario = request.user
            endereco.empresa = request.user.empresa

            # verifica se é o primeiro endereco, se sim torna-lo padrao
            enderecos = Endereco.objects.filter(usuario=request.user, empresa=request.user.empresa, status=True)
            if len(enderecos) == 0:
                endereco.padrao = True

            endereco.save()

            return redirect('empresas:empresa_endereco')
    else:
        form = EnderecoForm()

    estados = buscar_estados_api()
    contexto = {'form': form, 'estados': estados}

    return render(request, 'empresas/endereco/empresa-endereco-adicionar.html', contexto)

@login_required(login_url='/usuarios/login')
def editar_endereco(request):
    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])

    if len(request.POST) > 2:

        endereco = verificar_endereco_editar(request.POST['endereco'],
            request.POST['estado'],
            request.POST['cidade'],
            request.POST['cep'],
            request.POST['bairro'],
            request.POST['rua'],
            request.POST['numero'],
            request.POST['complemento']
        )

        return redirect('empresas:empresa_endereco')

    else:
        cidades = buscar_cidades_api(endereco.estado.sigla)
        nome_cidades = list(cidades.values())
        estados = buscar_estados_api()
        contexto = {'endereco': endereco, 'estados': estados, 'cidades': nome_cidades}

        return render(request, 'empresas/endereco/empresa-endereco-editar.html', contexto)

@login_required(login_url='/usuarios/login')
def deletar_endereco(request):
    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])
    era_padrao = endereco.padrao
    endereco.padrao = False
    endereco.status = False
    endereco.save()

    if era_padrao:
        enderecos = Endereco.objects.filter(usuario=request.user, empresa=request.user.empresa, status=True)

        # se o endereço deletado era padrão e houver outro, trocar automaticamente
        if len(enderecos) > 0:
            endereco = get_object_or_404(Endereco, pk=enderecos[0].pk)
            endereco.padrao = True
            endereco.save()

    return redirect('empresas:empresa_endereco')

@login_required(login_url='/usuarios/login')
def definir_endereco_padrao(request):
    enderecos = Endereco.objects.filter(usuario=request.user, empresa=request.user.empresa, padrao=True)

    if len(enderecos) > 0:
        endereco = get_object_or_404(Endereco, pk=enderecos[0].pk)
        endereco.padrao = False
        endereco.save()

    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])
    endereco.padrao = True
    endereco.save()

    return redirect('empresas:empresa_endereco')
