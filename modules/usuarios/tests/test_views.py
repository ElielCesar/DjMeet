from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from modules.usuarios.models import UserProfile


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
      
      
    def test_login_sucesso(self):
        self.client.logout()
        self.client.login(username=self.username, senha=self.password)
        resposta = self.client.get(self.url_novo_evento, follow=True)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(self.url_novo_evento in resposta.redirect_chain[0][0])
        

    def test_login_falha(self):
        self.client.logout()
        login = self.client.login(username=self.username, password='aaaa')
        resposta = self.client.get(reverse('novo_evento'))
        
        self.assertFalse(login)
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue('_auth_user_id' not in self.client.session)
        self.assertTrue(resposta['Location'].startswith(self.url_login))
        
        

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
