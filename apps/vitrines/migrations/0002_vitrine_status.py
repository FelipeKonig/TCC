# Generated by Django 3.1.4 on 2021-01-20 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitrines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitrine',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Ativo?'),
        ),
    ]