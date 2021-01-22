import requests
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from ..forms import EnderecoForm
from ..models import Cidade, Estado, Endereco

logger = logging.getLogger(__name__)


@login_required(login_url='/usuarios/login')
def perfil_endereco(request):
    enderecos = Endereco.objects.filter(usuario=request.user, status=True)

    return render(request, 'usuarios/endereco/perfil-endereco.html', {'enderecos': enderecos})


@login_required(login_url='/usuarios/login')
def adicionar_endereco(request):
    if request.method == "POST":

        dicionario = verificar_estado_cidade_bd(request.POST['estado'], request.POST['cidade'])
        novo_estado = dicionario[0]
        nova_cidade = dicionario[1]

        sigla = request.POST['estado'].split('|')[-1]
        nome = request.POST['estado'].split('|')[0]

        novo_estado = Estado.objects.get(nome=nome, sigla=sigla)

        nova_cidade = Cidade.objects.get(
            nome=request.POST['cidade'],
            estado_id=novo_estado.pk
        )

        novo_endereco = dict(
            estado=novo_estado,
            cidade=nova_cidade,
            cep=request.POST['cep'],
            bairro=request.POST['bairro'],
            rua=request.POST['rua'],
            numero=request.POST['numero'],
            complemento=request.POST['complemento']
        )
        form = EnderecoForm(novo_endereco)

        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user

            # verifica se é o primeiro endereco, se sim torna-lo padrao
            enderecos = Endereco.objects.filter(usuario=request.user)
            if len(enderecos) == 0:
                endereco.padrao = True

            endereco.save()

            return redirect('usuarios:perfil_endereco')
    else:
        form = EnderecoForm()

    estados = buscar_estados_api()
    contexto = {'form': form, 'estados': estados}

    return render(request, 'usuarios/endereco/perfil-endereco-formulario-adicionar.html', contexto)


@login_required(login_url='/usuarios/login')
def deletar_endereco(request):
    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])
    era_padrao = endereco.padrao
    endereco.padrao = False
    endereco.status = False
    endereco.save()

    if era_padrao:
        enderecos = Endereco.objects.filter(usuario=request.user, status=True)

        # se o endereço deletado era padrão e houver outro, trocar automaticamente
        if len(enderecos) > 0:
            endereco = get_object_or_404(Endereco, pk=enderecos[0].pk)
            endereco.padrao = True
            endereco.save()

    return redirect('usuarios:perfil_endereco')


@login_required(login_url='/usuarios/login')
def editar_endereco(request):
    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])

    if len(request.POST) > 2:

        sigla = request.POST['estado'].split('|')[-1]

        if endereco.estado.sigla != sigla:
            nome = request.POST['estado'].split('|')[0]
            novo_estado = Estado.objects.get(nome=nome, sigla=sigla)
            endereco.estado = novo_estado

        if endereco.cidade.nome != request.POST['cidade']:
            nova_cidade = Cidade.objects.get(
                nome=request.POST['cidade'],
                estado_id=endereco.estado.pk
            )
            endereco.cidade = nova_cidade

        endereco.cep = request.POST['cep']
        endereco.bairro = request.POST['bairro']
        endereco.rua = request.POST['rua']
        endereco.numero = request.POST['numero']

        logger.debug(request.POST['complemento'])
        endereco.complemento = request.POST['complemento']

        endereco.save()

        return redirect('usuarios:perfil_endereco')

    else:
        cidades = buscar_cidades_api(endereco.estado.sigla)
        nome_cidades = list(cidades.values())
        estados = buscar_estados_api()
        contexto = {'endereco': endereco, 'estados': estados, 'cidades': nome_cidades}

        return render(request, 'usuarios/endereco/perfil-endereco-formulario-editar.html', contexto)


@login_required(login_url='/usuarios/login')
def definir_endereco_padrao(request):
    enderecos = Endereco.objects.filter(usuario=request.user, padrao=True)

    if len(enderecos) > 0:
        endereco = get_object_or_404(Endereco, pk=enderecos[0].pk)
        endereco.padrao = False
        endereco.save()

    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])
    endereco.padrao = True
    endereco.save()

    return redirect('usuarios:perfil_endereco')


# AJAX
def carregar_cidades(request):
    sigla = request.GET.get('estado').split('|')[-1]
    logger.debug('sigla: {}'.format(sigla))

    cidades = buscar_cidades_api(sigla)

    if request.is_ajax():
        return JsonResponse({'cidades': cidades})

# AJAX
def verificar_cep(request):
    cep = 'https://viacep.com.br/ws/{}/json/'.format(request.GET.get('cep'))
    requisicao_cep = requests.get(cep)

    try:
        lista = requisicao_cep.json()
    except ValueError:
        logger.critical("Não encontrou o cep")

    dicionario = {0: lista}

    if request.is_ajax():
        return JsonResponse({'cep': dicionario})

def verificar_estado_cidade_bd(estado, cidade):

    sigla = estado.split('|')[-1]
    nome = estado.split('|')[0]

    logger.debug(estado)
    logger.debug(nome)

    # consulta '.objects.get_or_create' retorna tupla
    buscar_estado = Estado.objects.get_or_create(nome = nome, sigla = sigla)
    # consulta '.objects.get' retorna objeto, como preciso da pk do respectivo objeto, faço nova consulta
    estado = Estado.objects.get(nome = nome, sigla = sigla)

    buscar_cidade = Cidade.objects.get_or_create(nome = cidade, estado_id = estado.pk)
    cidade = Cidade.objects.get(nome = cidade, estado_id = estado.pk)

    dicionario = {}
    dicionario[0] = estado
    dicionario[1] = cidade

    return dicionario
    

def buscar_estados_api():
    # busca na api do ibge os estados por ordem de nome
    # obs:Você pode copiar e colar o link no navegador para ver o arquivo Json gerado
    estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome'

    # indica que quero obter os dados dessa requisição através do método .get()
    requisicao_estados = requests.get(estados)

    dicionario = {}

    try:
        # indica que quero desserializar, no caso,
        # transformar as informações str para um dicionário através do método .json()
        lista = requisicao_estados.json()

        for indice, estados in enumerate(lista):
            # adiciona as tuplas com os estados
            dicionario[indice] = estados

    except ValueError:
        logger.critical("Não encontrou os estados")

    return dicionario


def buscar_cidades_api(sigla):
    cidades = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'.format(sigla)
    requisicao_cidades = requests.get(cidades)

    dicionario = {}

    try:
        lista = requisicao_cidades.json()

        for indice, cidades in enumerate(lista):
            # apenas filtrando os dados do objeto em cidades para pegar apenas o nome,
            # dessa forma facilita a manipulação dos dados com js
            dicionario[indice] = cidades.get('nome')
    except ValueError:
        logger.critical("Não encontrou as cidades")

    return dicionario
