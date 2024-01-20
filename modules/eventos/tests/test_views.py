from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from modules.eventos.models import Evento, Certificado
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import override_settings
from django.contrib.messages import get_messages
import os
import shutil


class Base_Teste_Config(TestCase):
    def setUp(self):
        self.usuario = 'teste'
        self.senha = '12345'
        self.user = User.objects.create_user(username=self.usuario, password=self.senha)
        os.makedirs('test_media')
        
        # arquivo de imagem em memória
        self.imagem_teste = SimpleUploadedFile(
            name = 'teste.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        self.dados = {
            'nome':'Testes unitários com TestCase',
            'descricao':'evento de teste',
            'data_inicio':'20240120',
            'data_termino':'20240120',
            'carga_horaria':'4',
            'cor_principal':'#000000',
            'cor_secundaria':'#0000ff',
            'cor_fundo':'#ffffff',
        }

        self.dados['logo'] = self.imagem_teste
        
        self.name_url_novo_evento = 'novo_evento'
        self.nome_evento = 'Testes unitários com TestCase'
        self.msg_evento_sucesso = "Evento cadastrado com sucesso!!"
        self.url_login = '/usuarios/login'
        
    def tearDown(self):
        diretorio_a_remover = 'test_media'
        shutil.rmtree(diretorio_a_remover)
    

class Novo_Evento_View_Test(Base_Teste_Config):
    
    def test_novo_evento_GET(self):    
        valida_login_required = self.client.get(reverse(self.name_url_novo_evento))
        
        login = self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.get(reverse(self.name_url_novo_evento))
        
        self.assertTrue(valida_login_required['Location'].startswith(self.url_login))
        self.assertTrue(login)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/novo_evento.html')
        
        
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_POST_sucesso(self):
        self.client.logout()
        valida_login_required = self.client.post(reverse(self.name_url_novo_evento))
        
        login = self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.post(reverse(self.name_url_novo_evento), self.dados, format='multipart')
        messages = list(get_messages(resposta.wsgi_request))
        
        self.assertTrue(valida_login_required['Location'].startswith(self.url_login))
        self.assertTrue(login)
        self.assertTrue(resposta['Location'].endswith('/eventos/novo_evento'))
        self.assertTrue(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertTrue(any(self.msg_evento_sucesso in str(mensagem) for mensagem in messages))
    
    
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_POST_falha(self):
        dados = {
            'nome':'Testes unitários com TestCase',
            'descricao':'e',
            'data_inicio':'20240122',
            'data_termino':'20240124',
            }
        
        login = self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.post(reverse(self.name_url_novo_evento), dados, format='multipart')
        messages = list(get_messages(resposta.wsgi_request))
        
        self.assertTrue(login)
        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertTrue(len(messages) > 0)
        
        
class Gerenciar_Evento_View_Test(Base_Teste_Config):
    def test_gerenciar_evento_GET(self):
        self.client.logout()
        valida_login_required = self.client.get(reverse('gerenciar_evento'))
        
        login = self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.get(reverse('gerenciar_evento'))
        
        self.assertTrue(valida_login_required['Location'].startswith(self.url_login))
        self.assertTrue(login)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/gerenciar_evento.html')

      