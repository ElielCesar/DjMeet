'''
Esperado: validar filtro de 3 eventos
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


def fazer_login(usuario, senha):
    wait = WebDriverWait(browser, 10)
    
    username = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
    password = wait.until(EC.visibility_of_element_located((By.NAME, 'senha')))
    btn_logar = browser.find_element(By.CLASS_NAME, 'btn-principal')
        
    username.send_keys(usuario)
    password.send_keys(senha)
    btn_logar.click()


def test_filtrar_evento():
    time.sleep(3)
    espera = WebDriverWait(browser, 10)
    browser.get('http://127.0.0.1:8000/eventos/gerenciar_evento/')
     
    for evento in ['Manipulando', 'Pytest', 'Django']:
       
        titulo = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'form-control')))
        btn_filtrar = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
        
        titulo.send_keys(evento)
        btn_filtrar.click()
        time.sleep(1)
        browser.refresh()
        assert evento in browser.page_source, f'Texto Não encontrado!'

    time.sleep(2)
        

if __name__ == '__main__':
    fazer_login('eliel', '12345')
    test_filtrar_evento()
