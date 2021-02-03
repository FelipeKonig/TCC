# Generated by Django 3.1.4 on 2021-02-01 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vitrines', '0004_auto_20210130_2145'),
        ('produtos', '0005_auto_20210131_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.OneToOneField(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='produtos.categoria'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='vitrine',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='vitrines.vitrine'),
        ),
    ]
