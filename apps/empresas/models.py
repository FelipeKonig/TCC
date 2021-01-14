import os
from uuid import uuid4

from django.db import models
from stdimage import StdImageField


def adicionar_imagem_logo(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join('logoEmpresa/', filename)


class Empresa(models.Model):
    razaoSocial = models.CharField('Razão social', max_length=60, help_text='Obrigatório')
    fantasia = models.CharField('Nome fantasia', max_length=60, help_text='Obrigatório')
    cnpj = models.CharField('CNPJ', max_length=14, help_text='Obrigatório')
    inscricaoEstadual = models.CharField('Inscrição Estadual', max_length=50, null=True, blank=True,
                                         help_text='Não obrigatório')
    inscricaoMunicipal = models.CharField('Inscrição Municipal', max_length=50, null=True, blank=True,
                                          help_text='Não obrigatório')
    logo = StdImageField('Logo da empresa', upload_to=adicionar_imagem_logo, null=True, help_text='Obrigatório')
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return '{} - {} - {}'.format(self.cnpj, self.razaoSocial, self.fantasia)
