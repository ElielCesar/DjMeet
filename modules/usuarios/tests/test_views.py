from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from modules.usuarios.models import UserProfile
from django.contrib.messages import get_messages


class Base_Test_Config(TestCase):
    def setUp(self):
        self.username = 'teste1'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        self.dados = {
            'username': 'testcase',
            'email': 'tescase@gmail.com',
            'senha': '12345',
            'confirmar_senha': '12345',
            'nome_completo': 'testecase cesar',
            'telefone': '1234567890',
            'cidade': 'Ariquemes',
            'estado': 'RO'
        }
        
        self.url_login = '/usuarios/login'
        self.url_cadastro = '/usuarios/cadastro'
        self.url_novo_evento = '/eventos/novo_evento/'


class Login_View_Test(Base_Test_Config):
    
    def test_login_get(self):
        self.client.logout()
        resposta = self.client.get(reverse('login')) 
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'usuarios/login.html')
      
      
    def test_login_post_sucesso(self):
        self.client.logout()
        resposta = self.client.post(reverse('login'), {
            'username':self.username, 'senha':self.password}, follow=True)
       
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue('/eventos/novo_evento/' in resposta.redirect_chain[0][0])
        self.assertTrue(resposta.wsgi_request.user.is_authenticated)
        

    def test_login_post_falha(self):
        self.client.logout()
        resposta = self.client.post(reverse('login'), {
            'username':self.username, 'senha':'aaa'}, follow=True)
        
        mensagens = list(get_messages(resposta.wsgi_request))
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue('/usuarios/login' in resposta.redirect_chain[0][0])
        self.assertIn('Usuário ou Senha incorretos', [str(mensagem) for mensagem in mensagens])
        self.assertFalse(resposta.wsgi_request.user.is_authenticated)
        
class Logout_View_Test(Base_Test_Config):
        
    def test_logout_get(self):
        self.client.logout()
        self.client.login(username=self.username, password=self.password) 
        resposta = self.client.get(reverse('logout'))
        user = resposta.wsgi_request.user
        
        self.assertEqual(resposta.status_code, 302)
        self.assertFalse(user.is_authenticated)
        self.assertTrue(resposta['Location'].startswith(self.url_login))
        
        
class Cadastro_View_Test(Base_Test_Config): 
         
    def test_cadastro_get(self):
        resposta = self.client.get(reverse('cadastro'))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'usuarios/cadastro.html')
        
        
    def test_cadastro_post_sucesso(self):
        resposta = self.client.post(reverse('cadastro'), self.dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(User.objects.filter(username='testcase').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testcase').exists())
        self.assertTrue(resposta['Location'].startswith(self.url_cadastro))
        
        
        
    def test_cadastro_post_falha(self):
        dados_invalidos = {
            'username': 'userfalha',
            # Campos omitidos para simular dados inválidos
        }
        resposta = self.client.post(reverse('cadastro'), dados_invalidos)
        self.assertEqual(resposta.status_code, 302) 
        self.assertFalse(User.objects.filter(username='userfalha').exists())
        self.assertTrue(resposta['Location'].startswith(self.url_cadastro))
