# Generated by Django 5.0 on 2024-01-01 02:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('descricao', models.TextField(max_length=500)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('carga_horaria', models.IntegerField()),
                ('logo', models.ImageField(upload_to='logo_evento')),
                ('cor_principal', models.CharField(max_length=7)),
                ('cor_secundaria', models.CharField(max_length=7)),
                ('cor_fundo', models.CharField(max_length=7)),
                ('criador', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
