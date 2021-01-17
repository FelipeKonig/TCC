from django.test import TestCase, Client
from django.urls import reverse
import json

from ..models import *
from model_mommy import mommy


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.usuario = mommy.make(CustomUsuario)
        cls.estado = mommy.make(Estado, nome='Santa Catarina', sigla='SC')
        cls.cidade = mommy.make(Cidade, nome='Canoinhas', estado=cls.estado)
        cls.endereco = mommy.make(Endereco,
                                  estado=cls.estado,
                                  cidade=cls.cidade,
                                  usuario=cls.usuario,
                                  padrao=True,
                                  status=True)

    def test_perfil_endereco(self):
        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        response = cliente.get(reverse('usuarios:perfil_endereco'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/endereco/perfil-endereco.html')

        cliente2 = Client()
        response = cliente2.get(reverse('usuarios:perfil_endereco'))
        # sera redirecionado para a tela de login pois não esta logado
        self.assertEquals(response.status_code, 302)

    def test_adicionar_endereco(self):
        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        # é necessário criar os objetos para fazer as consultas na função
        estado = Estado.objects.get(id=self.estado.pk)
        cidade = Cidade.objects.get(id=self.cidade.pk)
        endereco = Endereco.objects.get(id=self.endereco.pk)

        url = reverse('usuarios:perfil_endereco_adicionar')
        response = cliente.post(url, {
            'estado': 'Santa Catarina|SC',
            'cidade': 'Canoinhas',
            'cep': '89464028',
            'bairro': 'Jardim Esperança',
            'rua': 'Saulo de Carvalho',
            'numero': '1455',
            'complemento': ''
        })
        # caso adicionar o endereco, irá redirecionar para para outra pagina, status_code=302
        self.assertEquals(response.status_code, 302)

        # verifica se a sigla do estado do endereco criado na função é o mesmo
        self.assertEquals(endereco.estado.sigla, 'SC')
        self.assertEquals(endereco.cidade.nome, 'Canoinhas')

    def test_deletar_endereco(self):
        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        endereco = Endereco.objects.get(id=self.endereco.pk)
        url = reverse('usuarios:deletar_endereco')
        response = cliente.post(url, {'endereco': endereco.pk})

        self.assertEquals(endereco.padrao, True)
        self.assertEquals(endereco.status, True)
        self.assertEquals(response.status_code, 302)

        url = reverse('usuarios:deletar_endereco')
        response = cliente.post(url, {'endereco': '90'})

        self.assertEquals(response.status_code, 404)

    def test_editar_endereco(self):
        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        novo_estado = mommy.make(Estado, nome='Alagoas', sigla='AL')
        nova_cidade = mommy.make(Cidade, nome='Anadia', estado=novo_estado)

        endereco = Endereco.objects.get(id=self.endereco.pk)
        url = reverse('usuarios:editar_endereco')
        response = cliente.post(url, {
            'endereco': endereco.pk,
            'estado': 'Alagoas|AL',
            'cidade': 'Anadia',
            'cep': '89464028',
            'bairro': 'Jardim Esperança',
            'rua': 'Saulo de Carvalho',
            'numero': '1455',
            'complemento': 'casa'
        })
        self.assertEquals(response.status_code, 302)

        url = reverse('usuarios:editar_endereco')
        response = cliente.post(url, {
            'endereco': 90,
            'estado': 'Alagoas|AL',
            'cidade': 'Anadia',
            'cep': '89464028',
            'bairro': 'Jardim Esperança',
            'rua': 'Saulo de Carvalho',
            'numero': '1455',
            'complemento': 'casa'
        })
        self.assertEquals(response.status_code, 404)

        url = reverse('usuarios:editar_endereco')
        response = cliente.post(url, {'endereco': endereco.pk})
        self.assertEquals(response.status_code, 200)

    def test_definir_endereco_padrao(self):
        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)
        endereco = Endereco.objects.get(id=self.endereco.pk)

        url = reverse('usuarios:definir_endereco_padrao')
        response = cliente.post(url, {'endereco': endereco.pk})
        self.assertEquals(response.status_code, 302)

        url = reverse('usuarios:definir_endereco_padrao')
        response = cliente.post(url, {'endereco': 1000})
        self.assertEquals(response.status_code, 404)
