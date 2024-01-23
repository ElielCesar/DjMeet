from django.test import TestCase, Client
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
        # usuario criador dos eventos
        self.usuario = 'teste'
        self.senha = '12345'
        self.user = User.objects.create_user(username=self.usuario, password=self.senha)
        
        if not os.path.exists('test_media'):
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
        
        # criar eventos para o usuario eliel
        self.evento1 = Evento.objects.create(
            criador=self.user,
            nome = 'Evento 1',
            descricao = 'evento de teste 1',
            data_inicio = '20240613',
            data_fim = '20240613',
            carga_horaria = '8',
            logo = self.imagem_teste,
            cor_principal = '#000000',
            cor_secundaria = '#000080',
            cor_fundo = '#ffffff',
        )
        
        self.evento2 = Evento.objects.create(
            criador=self.user,
            nome = 'Evento 2',
            descricao = 'evento de teste 2',
            data_inicio = '20240615',
            data_fim = '20240615',
            carga_horaria = '8',
            logo = self.imagem_teste,
            cor_principal = '#000000',
            cor_secundaria = '#000080',
            cor_fundo = '#ffffff',
        )
        
        self.name_url_novo_evento = 'novo_evento'
        self.nome_evento = 'Testes unitários com TestCase'
        self.msg_evento_sucesso = "Evento cadastrado com sucesso!!"
        self.url_login = '/usuarios/login'
        
    def tearDown(self):
        self.client.logout()
        if os.path.exists('test_media'):
            shutil.rmtree('test_media')
    

class Novo_Evento_View_Test(Base_Teste_Config):
    
    def test_acesso_sem_login(self):
        resposta = self.client.get(reverse(self.name_url_novo_evento))
        
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta['Location'].startswith(self.url_login))
        
    
    def test_acesso_com_login(self):    
        self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.get(reverse(self.name_url_novo_evento))
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/novo_evento.html')
        
        
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_POST_sucesso(self):
        self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.post(reverse(self.name_url_novo_evento), self.dados, format='multipart', follow=True)
        messages = list(get_messages(resposta.wsgi_request))
        
        self.assertRedirects(resposta, reverse('novo_evento'))
        self.assertTrue(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertTrue(any(self.msg_evento_sucesso in str(mensagem) for mensagem in messages))
    
    
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_nome_descricao_muito_curto(self):
        self.client.login(username=self.usuario, password=self.senha)
        self.dados['nome'] = 'abc'
        
        resposta = self.client.post(reverse(self.name_url_novo_evento), self.dados, format='multipart')
        mensagens = list(get_messages(resposta.wsgi_request))
        
        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn('Os campos nome e descricão devem ter no mínimo 5 caracteres.', [str(msg) for msg in mensagens])
        
    
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_datas_invalidas(self):
        self.client.login(username=self.usuario, password=self.senha)
        self.dados['data_inicio'] = '11221'
        self.dados['data_termino'] = '1124'
        
        resposta = self.client.post(reverse(self.name_url_novo_evento), self.dados, format='multipart')
        mensagens = list(get_messages(resposta.wsgi_request))
        
        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn('Valor icorreto nos campos de data', [str(msg) for msg in mensagens])
        
        
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_datas_none(self):
        self.client.login(username=self.usuario, password=self.senha)
        self.dados['data_inicio'] = 'None'
        self.dados['data_termino'] = 'None'
        
        resposta = self.client.post(reverse(self.name_url_novo_evento), self.dados, format='multipart')
        mensagens = list(get_messages(resposta.wsgi_request))
        
        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn('Valor icorreto nos campos de data', [str(msg) for msg in mensagens])
    
    
    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_carga_horaria_invalida(self):
        self.client.login(username=self.usuario, password=self.senha)
        self.dados['carga_horaria'] = '0'
        
        resposta = self.client.post(reverse(self.name_url_novo_evento), self.dados, format='multipart')
        mensagens = list(get_messages(resposta.wsgi_request))
        
        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn('A carga horária tem que ser maior que 0', [str(msg) for msg in mensagens])
        
        
class Gerenciar_Evento_View_Test(Base_Teste_Config):  
    
    def test_acesso_sem_login(self):
        resposta = self.client.get(reverse('gerenciar_evento'))
        
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta['Location'].startswith(self.url_login))
     
        
    def test_acesso_com_login(self):
        self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.get(reverse('gerenciar_evento'))
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/gerenciar_evento.html')
        self.assertEqual(len(resposta.context['eventos']), 2) # anotar isso no git
     
        
    def test_filtrar_eventos(self):
        self.client.login(username=self.usuario, password=self.senha)
        resposta = self.client.get(reverse('gerenciar_evento'), {'nome':'Evento 1'}) # isso simula filtro
        
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context['eventos']), 1)
        self.assertEqual(resposta.context['eventos'][0].nome, 'Evento 1')
        
 
class Base_Teste_Config_2(TestCase):
    def setUp(self):
        self.criador = 'eliel'
        self.senha = '12345'
        self.participante = 'participante'
        self.participante2 = 'participante2'
        
        self.user = User.objects.create_user(username=self.criador, password=self.senha)
        self.part = User.objects.create_user(username=self.participante, password=self.senha)
        self.part2 = User.objects.create_user(username=self.participante2, password=self.senha)
        
        # arquivo de imagem em memória
        self.imagem_teste = SimpleUploadedFile(
            name = 'teste.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        # cria um evento para testar a inscricao
        self.eventox = Evento.objects.create(
            criador=self.user,
            nome = 'testcase e pytest',
            descricao = 'evento de teste',
            data_inicio = '20240613',
            data_fim = '20240613',
            carga_horaria = '8',
            logo = self.imagem_teste,
            cor_principal = '#000000',
            cor_secundaria = '#000080',
            cor_fundo = '#ffffff',
        )
        
        self.certificado = Certificado.objects.create(
            certificado = self.imagem_teste,
            participante = self.part,
            evento = self.eventox,
            certificado_id = 'CERT1234567912'
        )
        
        self.inscrever_url = reverse('inscrever_evento', args=[self.eventox.id])
        self.participantes_url = reverse('participantes_evento', args=[self.eventox.id])
    
    
    def tearDown(self):
        self.client.logout()
        if os.path.exists('test_media'):
            shutil.rmtree('test_media')

           
class Inscrever_Evento_View_Test(Base_Teste_Config_2):
    
    # todos os testes aqui    
    def test_inscrever_evento_sem_login(self):
        resposta = self.client.get(self.inscrever_url)
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta['Location'].startswith('/usuarios/login'))
        self.assertFalse(resposta.wsgi_request.user.is_authenticated)
        
        
    def test_inscrever_evento_com_login(self):
        self.client.login(username=self.participante, password=self.senha)
        resposta = self.client.get(self.inscrever_url)
        
        self.assertTrue(resposta.wsgi_request.user.is_authenticated)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/inscrever_evento.html')
        self.assertIsNotNone(resposta.context['evento'])
        self.assertEqual(resposta.context['evento'].nome, 'testcase e pytest')
        
    
    def test_inscrever_evento_post(self):
        self.client.login(username=self.participante, password=self.senha)
        resposta = self.client.post(self.inscrever_url, follow=True)
        
        self.eventox.refresh_from_db()
        self.assertIn(self.part, self.eventox.participantes.all())
        self.assertRedirects(resposta, self.inscrever_url)
        
        mensagens = list(resposta.context['messages'])
        self.assertEqual(len(mensagens), 1)
        self.assertEqual(str(mensagens[0]), 'Inscricao realizada com sucesso!')    

class Meus_Eventos_View_Test(Base_Teste_Config_2):
    
    def test_meus_eventos(self):
        self.client.login(username=self.participante, password=self.senha)
        self.client.post(self.inscrever_url)
        
        self.eventox.refresh_from_db()
        resposta = self.client.get(reverse('meus_eventos'))
        
        self.assertIn(self.part, self.eventox.participantes.all())
        self.assertTemplateUsed(resposta, 'eventos/meus_eventos.html')
        self.assertEqual(resposta.context['eventos'][0].nome, 'testcase e pytest')
 
 
class Participantes_Evento_View_Test(Base_Teste_Config_2):
    
    def test_acesso_usuario_nao_criador(self):
        self.client.login(username=self.participante, password=self.senha)
        resposta = self.client.get(self.participantes_url, follow=True)
        mensagens = list(resposta.context['messages'])
        
        self.assertEqual('Esse evento não é seu.', str(mensagens[0]))
    
    def test_acesso_usuario_criador(self):
        self.client.login(username=self.criador, password=self.senha)
        resposta = self.client.get(self.participantes_url, follow=True)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/participantes_evento.html')
        self.assertEqual(resposta.context['evento'], self.eventox)
        self.assertEqual(list(resposta.context['participantes']), list(self.eventox.participantes.all()))
    

class Certificados_View_Test(Base_Teste_Config_2):
    
    def test_validar_certificado_get(self):
        resposta = self.client.get(reverse('validar_certificado'))
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/validar_certificado.html')
        
    def test_validar_certificado_invalido(self):
        resposta = self.client.post(reverse('validar_certificado'), {'cert_id':'1232'}, follow=True)
        mensagem = list(resposta.context['messages'])
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/validar_certificado.html')
        self.assertEqual('Certificado não encontrado!', str(mensagem[0]))
        
    
    def test_procurar_certificado_nao_sendo_criador(self):
        self.client.login(username=self.participante, password=self.senha)
        resposta = self.client.get(reverse('procurar_certificado', args=[self.eventox.id]), follow=True)
        mensagem = list(resposta.context['messages'])
        
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual('Você não ter permissão para acessar esse evento!', str(mensagem[0]))
        self.assertRedirects(resposta, reverse('gerenciar_evento'))
        
    def test_procurar_certificado_sendo_criador(self):
        self.client.login(username=self.criador, password=self.senha)
        resposta = self.client.post(reverse('procurar_certificado', args=[self.eventox.id]),
                                    {'email':'eliel.tecinfo@gmail.com'}, follow=True)
        
        mensagem = list(resposta.context['messages'])
        
        self.assertEqual(resposta.status_code, 200)
        self.assertRedirects(resposta, f'/eventos/certificados_evento/{self.eventox.id}/')
        self.assertEqual('Certificado não encontrado!', str(mensagem[0]))
    
    def test_meus_certificados_vazio(self):
        self.client.login(username=self.participante2, password=self.senha)
        resposta = self.client.get(reverse('meus_certificados'), follow=True)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'eventos/meus_certificados.html')
        self.assertIn('certificados', resposta.context)
        
        
#http://127.0.0.1:8000/eventos/certificados_evento/12/