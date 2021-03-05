from django.db import models

from mysite import settings


class Vitrine(models.Model):
    nome = models.CharField('Nome', max_length=60, help_text='Obrigatório')
    descricao = models.CharField('Descrição', max_length=450, help_text='Obrigatório')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Vitrine'
        verbose_name_plural = 'Vitrines'

    def __str__(self):
        return '{}-{}'.format(self.nome, self.descricao)
