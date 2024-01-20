'''
Esperado: Cadastrar 3 eventos com sucesso!
OBS: Esse teste terá de ser refatorado quando o campo
número de vagas for incrementado.
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

dataset1 = [
    'Criando sistemas com Django',
    'Aprenda a criar sistemas com django e se torne um dev!',
    '22/01/2024', '23/01/2024','8',
    'C:\\Users\\eliel\\Downloads\\eventos\\django.png',
    ]

dataset2 = [
    'Testes unitários com Pytest',
    'Aprenda a testar seu código',
    '26/01/2024', '26/01/2024','4',
    'C:\\Users\\eliel\\Downloads\\eventos\\python.png',
    ]

dataset3 = [
    'Manipulando elementos web com JS',
    'Aprenda a manipular elementos like a pro!',
    '26/01/2024','26/01/2024','4',
    'C:\\Users\\eliel\\Downloads\\eventos\\js.png',
    ]


def fazer_login(usuario, senha):
    wait = WebDriverWait(browser, 10)
    
    username = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
    password = wait.until(EC.visibility_of_element_located((By.NAME, 'senha')))
    btn_logar = browser.find_element(By.CLASS_NAME, 'btn-principal')
        
    username.send_keys(usuario)
    password.send_keys(senha)
    btn_logar.click()


def test_cadastar_novo_evento():
    time.sleep(3)
    espera = WebDriverWait(browser, 10)
     
    for dataset in [dataset1, dataset2, dataset3]:
        nome_evento = espera.until(EC.visibility_of_element_located((By.NAME, 'nome')))
        descricao_evento = espera.until(EC.visibility_of_element_located((By.NAME, 'descricao')))
        data_inicio = espera.until(EC.visibility_of_element_located((By.NAME, 'data_inicio')))
        data_fim = espera.until(EC.visibility_of_element_located((By.NAME, 'data_termino')))
        carga_horaria = espera.until(EC.visibility_of_element_located((By.NAME, 'carga_horaria')))
        logo_evento = espera.until(EC.visibility_of_element_located((By.NAME, 'logo')))
        btn_criar_evento = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))

        nome_evento.send_keys(dataset[0])
        descricao_evento.send_keys(dataset[1])
        data_inicio.send_keys(dataset[2])
        data_fim.send_keys(dataset[3])
        carga_horaria.send_keys(dataset[4])
        logo_evento.send_keys(dataset[5])

        btn_criar_evento.click()
        time.sleep(2)

        mensagem = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-success')))
        assert 'Evento cadastrado com sucesso!!' in mensagem.text, f'Mensagem incorreta'

        browser.refresh()

    browser.get('http://127.0.0.1:8000/eventos/gerenciar_evento/')
    time.sleep(10)
        

if __name__ == '__main__':
    fazer_login('eliel', '12345')
    test_cadastar_novo_evento()
