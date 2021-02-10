# Generated by Django 3.1.4 on 2021-02-10 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vitrines', '0001_initial'),
        ('produtos', '0003_auto_20210209_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='vendedor',
        ),
        migrations.AlterField(
            model_name='atributo',
            name='caracteristica',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='produtos.caracteristica'),
        ),
        migrations.AlterField(
            model_name='caracteristica',
            name='produto',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='produtos.produto'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='produtos.categoria'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='vitrine',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='vitrines.vitrine'),
        ),
    ]
