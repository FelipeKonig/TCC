# Generated by Django 3.1.4 on 2021-03-05 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vitrines', '0002_delete_avaliacao'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produtos', '0003_auto_20210305_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='numero_acessos',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(default=0, verbose_name='Nota')),
                ('quantidade', models.PositiveIntegerField(default=0, verbose_name='Quantidade')),
                ('observacao', models.TextField(help_text='Não obrigatório', max_length=250, null=True, verbose_name='Observação')),
                ('cliente', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('produto', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='produtos.produto')),
                ('vitrine', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='vitrines.vitrine')),
            ],
            options={
                'verbose_name': 'Avaliação',
                'verbose_name_plural': 'Avaliações',
            },
        ),
    ]
