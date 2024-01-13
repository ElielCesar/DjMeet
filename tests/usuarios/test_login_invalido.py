'''
Esperado: ao entrar com usuário ou senha inválida, uma mensagem de erro
deve ser retornada na tela de login.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# caminho para o webdriver e setup inicial
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
os.environ['PATH'] += os.pathsep + diretorio_atual
browser = webdriver.Chrome()
browser.get('http://127.0.0.1:8000/usuarios/login/')
browser.maximize_window()

# Datasets para validar logins
datasets = [
    ('teste1', '1234ee'),
    ('teste1', ''),
    ('teste1', 'teste1ee'),
    ('', '')
]

def test_validar_login(mensagem_esperada, css_seletor):
    wait = WebDriverWait(browser, 10)
    
    for usuario, senha_valor in datasets:
        username = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        senha = wait.until(EC.visibility_of_element_located((By.NAME, 'senha')))
        btn_logar = browser.find_element(By.CLASS_NAME, 'btn-principal')
        
        username.send_keys(usuario)
        senha.send_keys(senha_valor)
        btn_logar.click()

        mensagem_mostrada = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_seletor)))
        assert mensagem_esperada in mensagem_mostrada.text, "A mensagem de erro não é a mensagem esperada!"

        time.sleep(2)

        browser.refresh()

    print('Teste test_validar_login() executado com sucesso!')

if __name__ == '__main__':
    test_validar_login('Usuário ou Senha incorretos', '.alert.alert-danger')
