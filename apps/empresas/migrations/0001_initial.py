# Generated by Django 3.1.4 on 2021-02-25 19:16

import apps.empresas.models
import apps.empresas.validadoresForm
from django.db import migrations, models
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razaoSocial', models.CharField(help_text='Obrigatório', max_length=60, verbose_name='Razão social')),
                ('fantasia', models.CharField(help_text='Obrigatório', max_length=60, verbose_name='Nome fantasia')),
                ('cnpj', models.CharField(help_text='Obrigatório', max_length=18, validators=[apps.empresas.validadoresForm.validar_cnpj], verbose_name='CNPJ')),
                ('inscricaoEstadual', models.CharField(blank=True, help_text='Não obrigatório', max_length=50, null=True, verbose_name='Inscrição Estadual')),
                ('inscricaoMunicipal', models.CharField(blank=True, help_text='Não obrigatório', max_length=50, null=True, verbose_name='Inscrição Municipal')),
                ('logo', stdimage.models.StdImageField(help_text='Obrigatório', null=True, upload_to=apps.empresas.models.adicionar_imagem_logo, verbose_name='Logo da empresa')),
                ('status', models.BooleanField(default=True, verbose_name='Ativo?')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
    ]
