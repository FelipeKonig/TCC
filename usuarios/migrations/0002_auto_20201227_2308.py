# Generated by Django 3.1.4 on 2020-12-28 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidade',
            name='nome',
            field=models.CharField(help_text='Obrigatório', max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='customusuario',
            name='cpf',
            field=models.CharField(help_text='Obrigatório', max_length=11, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='customusuario',
            name='data_nascimento',
            field=models.DateField(help_text='Obrigatório', verbose_name='Data de nascimento'),
        ),
        migrations.AlterField(
            model_name='customusuario',
            name='email',
            field=models.EmailField(help_text='Obrigatório', max_length=254, unique=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='customusuario',
            name='first_name',
            field=models.CharField(help_text='Obrigatório', max_length=100, verbose_name='Primeiro nome'),
        ),
        migrations.AlterField(
            model_name='customusuario',
            name='last_name',
            field=models.CharField(help_text='Obrigatório', max_length=100, verbose_name='Último nome'),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='complemento',
            field=models.CharField(blank=True, help_text='Obrigatório', max_length=50, verbose_name='Complemento'),
        ),
        migrations.AlterField(
            model_name='estado',
            name='nome',
            field=models.CharField(help_text='Obrigatório', max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='numeroCelular',
            field=models.CharField(help_text='Obrigatório', max_length=30),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='numeroFixo',
            field=models.CharField(blank=True, help_text='Não obrigatório', max_length=30),
        ),
    ]
