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
        
    def tearDown(self):
        self.client.logout()


class Login_View_Test(Base_Test_Config):
    
    def test_login_get(self):
        self.url = reverse('login')
        self.template_esperado = 'usuarios/login.html'
        
        resposta = self.client.get(self.url)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, self.template_esperado)
      
      
    def test_login_post_sucesso(self):
        self.url = reverse('login')
        self.dados = {'username':self.username, 'senha':self.password}
        self.redirect_esperado = '/eventos/novo_evento/'
        
        resposta = self.client.post(self.url, self.dados, follow=True)
       
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(self.redirect_esperado in resposta.redirect_chain[0][0])
        self.assertTrue(resposta.wsgi_request.user.is_authenticated)
        

    def test_login_post_falha(self):
        self.url = reverse('login')
        self.dados = {'username':self.username, 'senha':'aaa'}
        self.msg_esperada = 'Usuário ou Senha incorretos'
        self.redirect_esperado = '/usuarios/login'
        
        resposta = self.client.post(self.url, self.dados, follow=True)
        mensagens = list(get_messages(resposta.wsgi_request))
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(self.redirect_esperado in resposta.redirect_chain[0][0])
        self.assertIn(self.msg_esperada, [str(msg) for msg in mensagens])
        self.assertFalse(resposta.wsgi_request.user.is_authenticated)
        
class Logout_View_Test(Base_Test_Config):
        
    def test_logout_get(self):
        self.url = reverse('logout')
        self.redirect_esperado = reverse('login')
       
        self.client.login(username=self.username, password=self.password) 
        resposta = self.client.get(self.url, follow=True)
        user = resposta.wsgi_request.user
        
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(user.is_authenticated)
        self.assertRedirects(resposta, self.redirect_esperado)
        
        
class Cadastro_View_Test(Base_Test_Config): 
         
    def test_cadastro_get(self):
        self.url = reverse('cadastro')
        self.template_esperado = 'usuarios/cadastro.html'
        
        resposta = self.client.get(self.url)
        
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, self.template_esperado)
        
    def test_cadastro_post_sucesso(self):
        self.url = reverse('cadastro')
        self.redirect_esperado = reverse('cadastro')
        
        resposta = self.client.post(self.url, self.dados, follow=True)
        
        self.assertTrue(User.objects.filter(username='testcase').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testcase').exists())
        self.assertRedirects(resposta, self.redirect_esperado)
        
    def test_cadastro_post_falha(self):
        self.url = reverse('cadastro')
        self.redirect_esperado = reverse('cadastro')
        dados_invalidos = {'username': 'userfalha', }
        # Campos omitidos para simular dados inválidos
        
        resposta = self.client.post(self.url, dados_invalidos, follow=True)
        
        self.assertEqual(resposta.status_code, 200) 
        self.assertFalse(User.objects.filter(username='userfalha').exists())
        self.assertRedirects(resposta, self.redirect_esperado)
