'''
Esperado: Ao executar esse teste, todos os campos devem acusar aviso
caso não sejam preenchido, exceto o campo estado por ser do tipo
select.
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
browser.get('http://127.0.0.1:8000/usuarios/cadastro/')
browser.maximize_window()


# dataset para o teste
dataset1 = ('Andrey Alencar', 'andrey', 'andrey@gmail.com','6999292-1212', 'Ariquemes', '1234', '1234')

def test_required_todos_campos():
    # tempo para voce reduzir o zoom da página
    time.sleep(5)  
    espera = WebDriverWait(browser, 10)

    nome_completo = espera.until(EC.visibility_of_element_located((By.NAME, 'nome_completo')))
    username = espera.until(EC.visibility_of_element_located((By.NAME, 'username')))
    email = espera.until(EC.visibility_of_element_located((By.NAME, 'email')))
    telefone = espera.until(EC.visibility_of_element_located((By.NAME, 'telefone')))
    cidade = espera.until(EC.visibility_of_element_located((By.NAME, 'cidade')))
    senha = espera.until(EC.visibility_of_element_located((By.NAME, 'senha')))
    confirmar_senha = espera.until(EC.visibility_of_element_located((By.NAME, 'confirmar_senha')))
    btn_cadastrar = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
    elementos = [nome_completo, username, email, telefone, cidade, senha, confirmar_senha]

    i = 0

    for elemento in elementos:
        elemento.send_keys(dataset1[i])
        btn_cadastrar.click()
        time.sleep(1)
        i += 1

    print('Teste test_required_todos_campos() executado com sucesso!')

if __name__ == '__main__':
    test_required_todos_campos()
    