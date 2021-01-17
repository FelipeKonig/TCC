import os

from uuid import uuid4
from django.db import models
from django.conf import settings
from stdimage.models import StdImageField
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from apps.empresas.models import Empresa


# Função para evitar duplicação de nomes de imagens, e renomear o nome da imagem com hash
# Adicionei o método os.path.join para separar as imagens de perfil, e assim, criar novos diretórios para imagens de
# outros objetos, tais como produtos
def adicionar_imagem_perfil(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join('perfil/', filename)


class Telefone(models.Model):
    # Com uma chave estrangeira do usuario em Telefone é possível o mesmo usuario criar vários telefones no 1..n
    # Deixei default="" porque o django não esta permitindo fazer a migração, provavelmente porque já estava no banco
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    # Não faz sentido o mesmo objeto telefone conter dois numeros, coloquei o atributo tipo para definir se é celular ou fixo
    # e deixei apenas um atributo de numero para o objeto
    tipo = models.CharField('Tipo', max_length=7, help_text='Obrigatório', default="")
    # numeroCelular = models.CharField('Telefone celular', blank=True, max_length=30, help_text='Não obrigatório')
    numero = models.CharField('Telefone fixo', max_length=30, help_text='Obrigatório', default="")
    padrao = models.BooleanField('Padrao', null=False, default=False)
    status = models.BooleanField('Status', null=False, default=True)

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'

    def __str__(self):
        return '{}, {}: {}'.format(self.usuario, self.tipo, self.numero)


class Estado(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Obrigatório')
    sigla = models.CharField('Sigla', max_length=5)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return "{} - ({})".format(self.nome, self.sigla)


class Cidade(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Obrigatório')
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    # Com uma chave estrangeira do usuario em Endereco é possível o mesmo usuario criar vários endereços no 1..n
    # Deixei default="" porque o django não esta permitindo fazer a migração, provavelmente porque já estava no banco
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    complemento = models.CharField('Complemento', max_length=50, blank=True, null=True, default="", help_text=' Não obrigatório')
    numero = models.CharField('Número', max_length=100, default='S/N', help_text='Obrigatório')
    # Se for um para um, vários endereços não poderão estar no mesmo estado e/ou cidade(objeto)
    # estado = models.OneToOneField(Estado, on_delete=models.PROTECT)
    # cidade = models.OneToOneField(Cidade, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    rua = models.CharField('Rua', max_length=100, help_text='Obrigatório')
    cep = models.CharField('CEP', max_length=25, help_text='Obrigatório')
    bairro = models.CharField('Bairro', max_length=50, help_text='Obrigatório')
    # Padrão seria o endereço escolhido para receber os pedidos para casos de houver mais de uma opção
    padrao = models.BooleanField('Padrao', null=False, default=False)
    status = models.BooleanField('Status', null=False, default=True)

    class Meta:
        verbose_name = 'Endereco'
        verbose_name_plural = 'Enderecos'

    def __str__(self):
        return '{}, cep: {}, numero: {}; status: {}'.format(
                self.usuario,
                self.cep,
                self.numero,
                self.status
            )


class UsuarioManager(BaseUserManager):
    use_in_migrations = True  # Estamos avisando ao Django, que esse será o nosso modelo que usaremos em nosso banco
    # de dados

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Fazendo método para criar usuário comum
    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # Fazendo método para criar super usuário
    def create_superuser(self, email, password, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)

        # Verificando se é super usuario
        if extrafields.get('is_superuser') is not True:
            raise ValueError('Super usuário precisa ter is_superuser como True')
        # Se for false o usuário não terá acesso ao painel administrativo do Django
        if extrafields.get('is_staff') is not True:
            raise ValueError('Super usuário precisa ter is_staff como True')

        return self._create_user(email, password, **extrafields)


class CustomUsuario(AbstractUser):
    first_name = models.CharField('Primeiro nome', max_length=100, help_text='Obrigatório')
    last_name = models.CharField('Último nome', max_length=100, help_text='Obrigatório')
    email = models.EmailField('E-mail', unique=True, help_text='Obrigatório')
    is_staff = models.BooleanField('Membro da equipe', default=True)
    status = models.BooleanField('Ativo?', default=False)

    # Se a chave estrangeira ficar no usuario, não vai ser possível fazer com que ele tenha vários endereços
    # telefone = models.ForeignKey(Telefone, on_delete=models.CASCADE, related_name='telefone', null=True)

    cpf = models.CharField('CPF', max_length=11, help_text='Obrigatório')
    data_nascimento = models.DateField('Data de nascimento', help_text='Obrigatório', null=True)

    # Problemas com o diretório e criação das fotos; está duplicando a mesma imagem com dois nomes diferentes
    # retirei o método variation e deixei null=True
    foto = StdImageField('Foto', upload_to=adicionar_imagem_perfil, null=True)
    #endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name='Endereço', null=True)
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, null=True)

    # Se a chave estrangeira ficar no usuario, não vai ser possível fazer com que ele tenha vários endereços
    # endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name='Endereço', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    objects = UsuarioManager()
