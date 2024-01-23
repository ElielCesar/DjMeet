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
        self.user = User.objects.create_user(
            username=self.usuario, password=self.senha)

        if not os.path.exists('test_media'):
            os.makedirs('test_media')

        # arquivo de imagem em memória
        self.imagem_teste = SimpleUploadedFile(
            name='teste.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        self.dados = {
            'nome': 'Testes unitários com TestCase',
            'descricao': 'evento de teste',
            'data_inicio': '20240120',
            'data_termino': '20240120',
            'carga_horaria': '4',
            'cor_principal': '#000000',
            'cor_secundaria': '#0000ff',
            'cor_fundo': '#ffffff',
        }

        self.dados['logo'] = self.imagem_teste

        # criar eventos para o usuario eliel
        self.evento1 = Evento.objects.create(
            criador=self.user,
            nome='Evento 1',
            descricao='evento de teste 1',
            data_inicio='20240613',
            data_fim='20240613',
            carga_horaria='8',
            logo=self.imagem_teste,
            cor_principal='#000000',
            cor_secundaria='#000080',
            cor_fundo='#ffffff',
        )

        self.evento2 = Evento.objects.create(
            criador=self.user,
            nome='Evento 2',
            descricao='evento de teste 2',
            data_inicio='20240615',
            data_fim='20240615',
            carga_horaria='8',
            logo=self.imagem_teste,
            cor_principal='#000000',
            cor_secundaria='#000080',
            cor_fundo='#ffffff',
        )

        
        

    def tearDown(self):
        self.client.logout()
        if os.path.exists('test_media'):
            shutil.rmtree('test_media')


class Novo_Evento_View_Test(Base_Teste_Config):

    def test_acesso_sem_login(self):
        self.url = reverse('novo_evento')
        self.url_login = '/usuarios/login'
        
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith(self.url_login))

    def test_acesso_com_login(self):
        self.url = reverse('novo_evento')
        self.template_esperado = 'eventos/novo_evento.html'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_esperado)

    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_POST_sucesso(self):
        self.url = reverse('novo_evento')
        self.msg_esperada = "Evento cadastrado com sucesso!!"
        self.nome_evento = 'Testes unitários com TestCase'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.post(self.url, self.dados, format='multipart', follow=True)
        messages = list(get_messages(resp.wsgi_request))

        self.assertRedirects(resp, self.url)
        self.assertTrue(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertTrue(any(self.msg_esperada in str(msg) for msg in messages))

    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_nome_descricao_muito_curto(self):
        self.url = reverse('novo_evento')
        self.msg_esperada = 'Os campos nome e descricão devem ter no mínimo 5 caracteres.'
        self.dados['nome'] = 'abc'
        self.nome_evento = 'Testes unitários com TestCase'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.post(self.url, self.dados, format='multipart')
        mensagens = list(get_messages(resp.wsgi_request))

        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn(self.msg_esperada, [str(msg) for msg in mensagens])

    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_datas_invalidas(self):
        self.url = reverse('novo_evento')
        self.msg_esperada = 'Valor icorreto nos campos de data'
        self.dados['data_inicio'] = '11221'
        self.dados['data_termino'] = '1124'
        self.nome_evento = 'Testes unitários com TestCase'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.post(self.url, self.dados, format='multipart')
        mensagens = list(get_messages(resp.wsgi_request))

        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn(self.msg_esperada, [str(msg) for msg in mensagens])

    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_datas_none(self):
        self.url = reverse('novo_evento')
        self.msg_esperada = 'Valor icorreto nos campos de data'
        self.dados['data_inicio'] = 'None'
        self.dados['data_termino'] = 'None'
        self.nome_evento = 'Testes unitários com TestCase'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.post(self.url, self.dados, format='multipart')
        mensagens = list(get_messages(resp.wsgi_request))

        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn(self.msg_esperada, [str(msg) for msg in mensagens])

    @override_settings(MEDIA_ROOT=(settings.BASE_DIR / 'test_media'))
    def test_novo_evento_carga_horaria_invalida(self):
        self.url = reverse('novo_evento')
        self.msg_esperada = 'A carga horária tem que ser maior que 0'
        self.dados['carga_horaria'] = '0'
        self.nome_evento = 'Testes unitários com TestCase'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.post(self.url, self.dados, format='multipart')
        mensagens = list(get_messages(resp.wsgi_request))

        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())
        self.assertIn(self.msg_esperada, [str(msg) for msg in mensagens])


class Gerenciar_Evento_View_Test(Base_Teste_Config):

    def test_acesso_sem_login(self):
        self.url = reverse('gerenciar_evento')
        self.url_login = '/usuarios/login'
        
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith(self.url_login))

    def test_acesso_com_login(self):
        self.url = reverse('gerenciar_evento')
        self.template_esperado = 'eventos/gerenciar_evento.html'
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_esperado)
        self.assertEqual(len(resp.context['eventos']), 2)

    def test_filtrar_eventos(self):
        self.url = reverse('gerenciar_evento')
        self.dados = {'nome': 'Evento 1'}
        
        self.client.login(username=self.usuario, password=self.senha)
        resp = self.client.get(self.url, self.dados)  

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['eventos']), 1)
        self.assertEqual(resp.context['eventos'][0].nome, 'Evento 1')


class Base_Teste_Config_2(TestCase):
    def setUp(self):
        self.criador = 'eliel'
        self.senha = '12345'
        self.participante = 'participante'
        self.participante2 = 'participante2'

        self.criador = User.objects.create_user(
            username=self.criador, password=self.senha)
        self.part = User.objects.create_user(
            username=self.participante, password=self.senha)
        self.part2 = User.objects.create_user(
            username=self.participante2, password=self.senha)

        # arquivo de imagem em memória
        self.imagem_teste = SimpleUploadedFile(
            name='teste.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        # cria um evento para testar a inscricao
        self.eventox = Evento.objects.create(
            criador=self.criador,
            nome='testcase e pytest',
            descricao='evento de teste',
            data_inicio='20240613',
            data_fim='20240613',
            carga_horaria='8',
            logo=self.imagem_teste,
            cor_principal='#000000',
            cor_secundaria='#000080',
            cor_fundo='#ffffff',
        )

        self.certificado = Certificado.objects.create(
            certificado=self.imagem_teste,
            participante=self.part,
            evento=self.eventox,
            certificado_id='CERT1234567912'
        )

        #self.inscrever_url = reverse('inscrever_evento', args=[self.eventox.id])
        #self.participantes_url = reverse('participantes_evento', args=[self.eventox.id])

    def tearDown(self):
        self.client.logout()
        if os.path.exists('test_media'):
            shutil.rmtree('test_media')


class Inscrever_Evento_View_Test(Base_Teste_Config_2):

    # todos os testes aqui
    def test_inscrever_evento_sem_login(self):
        self.inscrever_url = reverse('inscrever_evento', args=[self.eventox.id])
        
        resp = self.client.get(self.inscrever_url)
        
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith('/usuarios/login'))
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_inscrever_evento_com_login(self):
        self.inscrever_url = reverse('inscrever_evento', args=[self.eventox.id])
        self.template_esperado = 'eventos/inscrever_evento.html'
        self.nome_esperado = 'testcase e pytest'
        
        self.client.login(username=self.participante, password=self.senha)
        resp = self.client.get(self.inscrever_url)

        self.assertTrue(resp.wsgi_request.user.is_authenticated)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_esperado)
        self.assertIsNotNone(resp.context['evento'])
        self.assertEqual(resp.context['evento'].nome, self.nome_esperado)

    def test_inscrever_evento_post(self):
        self.inscrever_url = reverse('inscrever_evento', args=[self.eventox.id])
        self.msg_esperada = 'Inscricao realizada com sucesso!'
        
        self.client.login(username=self.participante, password=self.senha)
        resp = self.client.post(self.inscrever_url, follow=True)
        mensagens = list(resp.context['messages'])

        self.assertIn(self.part, self.eventox.participantes.all())
        self.assertRedirects(resp, self.inscrever_url)
        self.assertEqual(len(mensagens), 1)
        self.assertEqual(str(mensagens[0]), self.msg_esperada)


class Meus_Eventos_View_Test(Base_Teste_Config_2):

    def test_meus_eventos(self):
        self.inscrever_url = reverse('inscrever_evento', args=[self.eventox.id])
        self.url = reverse('meus_eventos')
        self.template_esperado = 'eventos/meus_eventos.html'
        self.nome_esperado = 'testcase e pytest'
        
        self.client.login(username=self.participante, password=self.senha)
        self.client.post(self.inscrever_url)
        resp = self.client.get(self.url)

        self.assertIn(self.part, self.eventox.participantes.all())
        self.assertTemplateUsed(resp, self.template_esperado)
        self.assertEqual(resp.context['eventos'][0].nome, self.nome_esperado)


class Participantes_Evento_View_Test(Base_Teste_Config_2):

    def test_acesso_usuario_nao_criador(self):
        self.msg_esperada = 'Esse evento não é seu.'
        self.url = reverse('participantes_evento', args=[self.eventox.id])
        
        self.client.login(username=self.participante, password=self.senha)
        resp = self.client.get(self.url, follow=True)
        mensagens = list(resp.context['messages'])

        self.assertEqual(self.msg_esperada, str(mensagens[0]))

    def test_acesso_usuario_criador(self):
        self.template_esperado = 'eventos/participantes_evento.html'
        self.url = reverse('participantes_evento', args=[self.eventox.id])
        
        self.client.login(username=self.criador, password=self.senha)
        resp = self.client.get(self.url, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_esperado)
        self.assertEqual(resp.context['evento'], self.eventox)
        self.assertEqual(list(resp.context['participantes']), list(
            self.eventox.participantes.all()))


class Certificados_View_Test(Base_Teste_Config_2):

    def test_validar_certificado_get(self):
        self.template_esperado = 'eventos/validar_certificado.html'
        self.url = reverse('validar_certificado')
        
        resp = self.client.get(self.url)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_esperado)

    def test_validar_certificado_invalido(self):
        self.url = reverse('validar_certificado')
        self.msg_esperada = 'Certificado não encontrado!'
        self.template_esperado = 'eventos/validar_certificado.html'
        self.dados = {'cert_id': '1232'}
        
        resp = self.client.post(self.url, self.dados, follow=True)
        mensagem = list(resp.context['messages'])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, self.template_esperado)
        self.assertEqual(self.msg_esperada, str(mensagem[0]))

    def test_procurar_certificado_nao_sendo_criador(self):
        self.url = reverse('procurar_certificado', args=[self.eventox.id])
        self.msg_esperada = 'Acesse seus certificados pelo menu Participantes > Meus Certificados'
        self.redirect_esperado = reverse('gerenciar_evento')
        
        self.client.login(username=self.participante, password=self.senha)
        resp = self.client.get(self.url, follow=True)
        mensagem = list(resp.context['messages'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.msg_esperada, str(mensagem[0]))
        self.assertRedirects(resp, self.redirect_esperado)

    def test_procurar_certificado_sendo_criador(self):
        self.url = reverse('procurar_certificado', args=[self.eventox.id])
        self.msg_esperada = 'Certificado não encontrado!'
        self.redirect_esperado = f'/eventos/certificados_evento/{self.eventox.id}/'
        self.dados = {'email': 'eliel.tecinfo@gmail.com'}
        
        self.client.login(username=self.criador, password=self.senha)
        resp = self.client.post(self.url, self.dados, follow=True)
        mensagem = list(resp.context['messages'])
        
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, self.redirect_esperado)
        self.assertEqual(self.msg_esperada, str(mensagem[0]))

    def test_meus_certificados_vazio(self):
        self.client.login(username=self.participante2, password=self.senha)
        resp = self.client.get(reverse('meus_certificados'), follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'eventos/meus_certificados.html')
        self.assertIn('certificados', resp.context)

    def test_gerar_certificado_nao_sendo_criador(self):
        self.url = reverse('gerar_certificado', args=[self.eventox.id])
        self.msg_esperada = 'Você não ter permissão para acessar esse evento!'
        self.client.login(username=self.participante2, password=self.senha)
        
        resp = self.client.get(self.url, follow=True)
        mensagem = list(resp.context['messages'])

        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, f'/eventos/gerenciar_evento/')
        self.assertEqual(self.msg_esperada, str(mensagem[0]))


class Deletar_Evento_View_Test(Base_Teste_Config_2):
    def test_deletar_evento_falha(self):
        self.url = reverse('deletar_evento', args=[self.eventox.id])
        self.redirect_esperado = reverse('gerenciar_evento')
        self.msg_esperada = 'Esse evento não é seu.'
        
        self.client.login(username=self.participante2, password=self.senha)
        resp = self.client.get(self.url, follow=True)
        mensagem = list(resp.context['messages'])
        
        self.assertRedirects(resp, self.redirect_esperado)
        self.assertEqual(self.msg_esperada, str(mensagem[0]))
    
    def test_deletar_evento_sucesso(self):
        self.nome_evento = 'testcase e pytest'
        self.url = reverse('deletar_evento', args=[self.eventox.id])
        self.redirect_esperado = reverse('gerenciar_evento')
        self.msg_esperada = 'Evento deletado com sucesso'
        
        self.client.login(username=self.criador, password=self.senha)
        resp = self.client.get(self.url, follow=True)
        mensagem = list(resp.context['messages'])
        
        self.assertRedirects(resp, self.redirect_esperado)
        self.assertEqual(self.msg_esperada, str(mensagem[0]))
        self.assertFalse(Evento.objects.filter(nome=self.nome_evento).exists())


class Editar_Evento_View_Test(Base_Teste_Config_2):
    def test_usuario_nao_autorizado(self):
        self.url = reverse('editar_evento', args=[self.eventox.id])
        self.redirect_esperado = reverse('gerenciar_evento')
        self.msg_esperada = 'Esse evento não é seu.'
        
        self.client.login(username=self.participante2, password=self.senha)
        resp = self.client.get(self.url, follow=True)
        mensagem = list(resp.context['messages'])
        
        self.assertRedirects(resp, self.redirect_esperado)
        self.assertEqual(self.msg_esperada, str(mensagem[0]))
    
    def test_simples_usuario_autorizado(self):
        self.url = reverse('editar_evento', args=[self.eventox.id])
        self.template_esperado = 'eventos/editar_evento.html'
        
        self.client.login(username=self.criador, password=self.senha)
        resp = self.client.get(self.url, follow=True)

        self.assertTemplateUsed(resp, self.template_esperado)
        self.assertIn('evento', resp.context)
            