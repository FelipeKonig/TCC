# a biblioteca requests é o padrão para fazer solicitações HTTP em Python
# utilizada no nosso caso para fazer a requisição da api do ibge e do viaCep
# obs: é necessário baixar ela no django, necessário baixar arquivos do requirements
import requests
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# As importações relativas usam pontos iniciais. Um único ponto inicial indica
# uma importação relativa, exemplo ".forms", começando com o pacote atual, que
# antes era apenas a pasta 'usuarios'. Dois ou mais pontos iniciais indicam uma
# importação relativa ao(s) pai(s) do pacote atual, que agora é 'usuarios/views'
# por isso está 'from ..forms import..' e não 'from .forms import..' como antes
from ..forms import EnderecoForm
from ..models import Cidade, Estado, Endereco

logger = logging.getLogger(__name__)

@login_required
def perfil_endereco(request):
    enderecos = Endereco.objects.filter(usuario=request.user, status = True)
    return render(request, 'usuarios/endereco/perfil-endereco.html', {'enderecos':enderecos})

@login_required
def endereco_formulario_adicionar(request):

    if request.method == "POST":

        sigla = request.POST['estado'].split('|')[-1]
        nome = request.POST['estado'].split('|')[0]

        novo_estado = Estado.objects.get(nome=nome, sigla=sigla)

        nova_cidade = Cidade.objects.get(
            nome = request.POST['cidade'],
            estado_id = novo_estado.pk
        )

        # criando o formulario pelo dicionario pois os selects no template
        # não fornecem os objetos estado e cidade, apenas os respectivos nomes
        # como o Endereco depende desses objetos para sua criação,
        # logicamente estou buscando pela própria função
        # obs: não preciso me preocupar com a busca dos objetos porque esta sendo
        # criado automaticamente por ajax enquanto o formulario é preenchido
        novo_endereco = dict(
            estado = novo_estado,
            cidade = nova_cidade,
            cep = request.POST['cep'],
            bairro = request.POST['bairro'],
            rua = request.POST['rua'],
            numero = request.POST['numero'],
            complemento = request.POST['complemento']
        )
        form = EnderecoForm(novo_endereco)

        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user

            #verifica se é o primeiro endereco, se sim torna-lo padrao
            enderecos = Endereco.objects.filter(usuario=request.user)
            if len(enderecos) == 0:
                endereco.padrao = True

            endereco.save()

            return redirect('usuarios:perfil_endereco')
    else:
        form = EnderecoForm()

    estados = buscar_estados_api()
    contexto = {'form': form, 'estados': estados }

    return render(request, 'usuarios/endereco/perfil-endereco-formulario-adicionar.html',contexto)

@login_required
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

@login_required
def editar_endereco(request):

    endereco = get_object_or_404(Endereco, pk=request.POST['endereco'])

    # se os atributos do Post forem acima de 2 itens, ele fará a edição
    # isso porque também é feito um Post para acessar o template de edição
    # para manter a confidencialidade dos dados durante a requisição
    # caso fosse uma requisição get para o template, seria possível visualizar
    # a pk de endereço através do navegador
    if len(request.POST) > 2:

        sigla = request.POST['estado'].split('|')[-1]

        if endereco.estado.sigla != sigla:
            nome = request.POST['estado'].split('|')[0]
            novo_estado = Estado.objects.get(nome=nome, sigla=sigla)
            endereco.estado = novo_estado

        if endereco.cidade.nome != request.POST['cidade']:
            nova_cidade = Cidade.objects.get(
                nome = request.POST['cidade'],
                estado_id = endereco.estado.pk
            )
            endereco.cidade = nova_cidade

        endereco.cep = request.POST['cep']
        endereco.bairro = request.POST['bairro']
        endereco.rua = request.POST['rua']
        endereco.numero = request.POST['numero']
        endereco.complemento = request.POST['complemento']

        endereco.save()

        return redirect('usuarios:perfil_endereco')

    else:
        cidades = buscar_cidades_api(endereco.estado.sigla)
        nome_cidades = list(cidades.values())
        estados = buscar_estados_api()
        contexto = {'endereco':endereco, 'estados':estados, 'cidades':nome_cidades}

        return render(request, 'usuarios/endereco/perfil-endereco-formulario-editar.html', contexto)


@login_required
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
def verificar_cidade_bd(request):

    sigla = request.GET.get('estado').split('|')[-1]
    nome = request.GET.get('estado').split('|')[0]

    buscar_estado = Estado.objects.get_or_create(nome = nome, sigla = sigla)
    estado = Estado.objects.get(nome = nome, sigla = sigla)

    buscar_cidade = Cidade.objects.get_or_create(nome = request.GET.get('cidade'), estado_id = estado.pk)
    cidade = Cidade.objects.get(nome = request.GET.get('cidade'), estado_id = estado.pk)

    dicionario = {}
    dicionario[0] = estado.pk
    dicionario[1] = cidade.pk

    if request.is_ajax():
        return JsonResponse({'dicionario': dicionario })

# AJAX
def verificar_cep(request):

    cep = 'https://viacep.com.br/ws/{}/json/'.format(request.GET.get('cep'))
    requisicao_cep = requests.get(cep)

    try:
        lista = requisicao_cep.json()
    except ValueError:
        logger.critical("Não encontrou o cep")

    dicionario = {}
    dicionario[0] = lista

    if request.is_ajax():
        return JsonResponse({'cep': dicionario })

def buscar_estados_api():

    # busca na api do ibge os estados por ordem de nome
    # obs:Você pode copiar e colar o link no navegador para ver o arquivo Json gerado
    estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome'

    # indica que quero obter os dados dessa requisição através do método .get()
    requisicao_estados = requests.get(estados)

    try:
        # indica que quero desserializar, no caso,
        # transformar as informações str para um dicionário através do método .json()
        lista = requisicao_estados.json()
    except ValueError:
        logger.critical("Não encontrou os estados")

    dicionario = {}

    # enumerate é usado em loops for ou ser convertido em uma lista de tuplas usando o método list()
    # ou seja, através do enumerate cria tuplas dos estados de acordo com o indice
    # se olhar o arquivo completo acessando o link acima fica mais fácil de entender o motivo
    for indice, estados in enumerate(lista):
        # adiciona as tuplas com os estados
        dicionario[indice] = estados

    return dicionario

def buscar_cidades_api(sigla):

    cidades = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'.format(sigla)
    requisicao_cidades = requests.get(cidades)

    try:
        lista = requisicao_cidades.json()
    except ValueError:
        logger.critical("Não encontrou as cidades")

    dicionario = {}
    for indice, cidades in enumerate(lista):

        # apenas filtrando os dados do objeto em cidades para pegar apenas o nome
        dicionario[indice] = cidades.get('nome')

    return dicionario
