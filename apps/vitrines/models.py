from django.db import models

from mysite import settings


class Vitrine(models.Model):
    nome = models.CharField('Nome', max_length=60, help_text='Obrigatório')
    descricao = models.CharField('Descrição', max_length=200, help_text='Obrigatório')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Vitrine'
        verbose_name_plural = 'Vitrines'

    def __str__(self):
        return '{}-{}'.format(self.nome, self.descricao)


class Avaliacao(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    nota = models.IntegerField('Nota', default=0)
    observacao = models.TextField('Observação', max_length=250, help_text='Não obrigatório', null=True)
    vitrine = models.ForeignKey(Vitrine, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
