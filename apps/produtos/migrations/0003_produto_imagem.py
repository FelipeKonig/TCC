# Generated by Django 3.1.4 on 2021-01-31 01:04

import apps.produtos.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_auto_20210130_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=stdimage.models.StdImageField(default=1, help_text='Obrigatório', upload_to=apps.produtos.models.adicionar_imagem_logo, verbose_name='Imagem do produto'),
            preserve_default=False,
        ),
    ]