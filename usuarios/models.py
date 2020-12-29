import uuid

from django.db import models
from phone_field import PhoneField
from stdimage.models import StdImageField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Função para evitar duplicação de nomes de imagens, e renomear o nome da imagem com hash
def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Telefone(models.Model):
    numeroCelular = models.CharField('Telefone celular', max_length=30, help_text='Obrigatório')
    numeroFixo = models.CharField('Telefone fixo', blank=True, max_length=30, help_text='Não obrigatório')

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'

    def __str__(self):
        return self.numeroCelular


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
    complemento = models.CharField('Complemento', max_length=50, blank=True, help_text=' Não obrigatório')
    numero = models.CharField('Número', max_length=100, default='S/N', help_text='Obrigatório')
    estado = models.OneToOneField(Estado, on_delete=models.PROTECT)
    cidade = models.OneToOneField(Cidade, on_delete=models.PROTECT)
    rua = models.CharField('Rua', max_length=100, help_text='Obrigatório')
    cep = models.CharField('CEP', max_length=25, help_text='Obrigatório')
    bairro = models.CharField('Bairro', max_length=50, help_text='Obrigatório')


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
    # fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)
    telefone = models.ForeignKey(Telefone, on_delete=models.CASCADE, related_name='telefone')
    cpf = models.CharField('CPF', unique=True, max_length=11, help_text='Obrigatório')
    data_nascimento = models.DateField('Data de nascimento', help_text='Obrigatório')
    foto = StdImageField('Foto', upload_to=get_file_path,
                         variations={'thumb': {'width': 400, 'height': 400, 'crop': True}})
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name='Endereço')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone', 'cpf', 'data_nascimento', 'foto', 'endereco']

    def __str__(self):
        return self.email

    objects = UsuarioManager()
