from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Evento(models.Model):
    criador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.TextField(max_length=500)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    carga_horaria = models.IntegerField(null=False, blank=False)
    logo = models.ImageField(upload_to='logo_evento')
    participantes = models.ManyToManyField(User, related_name='evento_participante', null=True, blank=True)

    # paleta de cores
    cor_principal = models.CharField(max_length=7)
    cor_secundaria = models.CharField(max_length=7)
    cor_fundo = models.CharField(max_length=7)

    def __str__(self):
        return self.nome

def pasta_certificado_evento(instance, filename):
    
    subpasta = f'certificados/evento{instance.evento.id}'
    caminho_arquivo = os.path.join(subpasta, filename)
    return caminho_arquivo
    
class Certificado(models.Model):
    
    certificado = models.ImageField(upload_to=pasta_certificado_evento)
    participante = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='certificados')
    certificado_id = models.CharField(max_length=10, unique=True)
    