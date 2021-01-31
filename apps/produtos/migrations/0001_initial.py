# Generated by Django 3.1.4 on 2021-01-31 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Obrigatório', max_length=200, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Não obrigatório', max_length=200, verbose_name='Nome')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='produtos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Obrigatório', max_length=250, verbose_name='Nome')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço')),
                ('descricao', models.CharField(max_length=450, verbose_name='Descrição')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('vendedor', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=200, verbose_name='Tópico')),
                ('descricao', models.CharField(max_length=450, verbose_name='Descrição')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
            ],
            options={
                'verbose_name': 'Característica',
                'verbose_name_plural': 'Características',
            },
        ),
    ]