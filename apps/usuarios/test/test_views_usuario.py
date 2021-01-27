from django.test import TestCase, Client
from django.urls import reverse

from ..models import *
from model_mommy import mommy


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.usuario = mommy.make(CustomUsuario, foto='perfil/2ac3aacf3d8748209eea7ca8a7b6376c.jpg')

    def test_perfil_principal(self):

        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        response = cliente.get(reverse('usuarios:perfil_principal'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/dados_perfil_usuario.html')

    # obs: enquanto a foto do usuario ser obrigatória, se você não colocar uma foto
    # que está no seu arquivo 'media/perfil/', o django não vai encontrar a foto do usuario e daí vai dar erro
    def test_perfil_configuracao(self):

        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        response = cliente.get(reverse('usuarios:perfil_configuracao'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil-configuracao.html')
