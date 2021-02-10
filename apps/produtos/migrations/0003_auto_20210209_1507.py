# Generated by Django 3.1.4 on 2021-02-09 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_auto_20210203_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caracteristica',
            name='descricao',
        ),
        migrations.AlterField(
            model_name='caracteristica',
            name='produto',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='produtos.produto'),
        ),
        migrations.CreateModel(
            name='Atributo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('descricao', models.CharField(max_length=450, verbose_name='Descrição')),
                ('caracteristica', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='produtos.caracteristica')),
            ],
            options={
                'verbose_name': 'Atributo',
                'verbose_name_plural': 'Atributos',
            },
        ),
    ]
