import uuid

from django.test import TestCase, Client
from django.urls import reverse
from model_mommy import mommy
from ..models import Empresa, adicionar_imagem_logo
from ...usuarios.models import CustomUsuario


class Test_Views(TestCase):
    def setUp(self):
        self.usuario = mommy.make(CustomUsuario)
        self.filename = f'{uuid.uuid4()}.png'
        self.empresa = mommy.make(Empresa,
                                  razaoSocial='Gráfica Ltda',
                                  fantasia='Gráfica Ltda',
                                  cnpj='13805125000130',
                                  inscricaoEstadual='245624856',
                                  inscricaoMunicipal='231645654',
                                  logo=self.filename,
                                  status=True
                                  )

        self.empresa.save()
        self.usuario.save()

    def test_cadastro_empresa(self):
        usuario = CustomUsuario.objects.get(email=self.usuario.email)

        cliente = Client()

        login = cliente.force_login(usuario)
        empresa = Empresa.objects.get(id=self.empresa.id)

        url = reverse('empresas:criar_empresa')

        context = {
            'razaoSocial': 'Gráfica Ltda',
            'fantasia': 'Gráfica Ltda',
            'cnpj': '13805125000130',
            'inscricaoEstadual': '245624856',
            'inscricaoMunicipal': '231645654',
            'logo': self.filename
        }

        response = cliente.post(url, context)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(empresa.fantasia, 'Gráfica Ltda')
        self.assertEquals(empresa.cnpj, '13805125000130')

    # def test_deletar_empresa(self):
    #     usuario = CustomUsuario.objects.get(email=self.usuario.email)
    #     cliente = Client()
    #     login = cliente.force_login(usuario)
    #
    #     empresa = Empresa.objects.get(cnpj=self.empresa.cnpj)
    #     url = reverse('empresas:deletar_empresa', kwargs={'pk': 1})
    #     response = cliente.post(url, {'pk': empresa.id})
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(empresa.status, True)






class LogoEmpresaTestCase(TestCase):

    def setUp(self):
        self.filename = f'{uuid.uuid4()}.png'  # Criando arquivo para realizar comparação

    def test_get_file_path(self):
        arquivo = adicionar_imagem_logo(None, 'teste.png')
        self.assertTrue(len(arquivo), len(self.filename))
