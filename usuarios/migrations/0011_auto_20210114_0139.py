# Generated by Django 3.1.4 on 2021-01-14 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_auto_20210112_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='complemento',
            field=models.CharField(blank=True, default='', help_text=' Não obrigatório', max_length=50, null=True, verbose_name='Complemento'),
        ),
    ]