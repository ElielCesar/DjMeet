'''
esperado: Testar a funcionalidade do icone de copiar link,
para isso é necessário um usuário que tenha pelo menos 2 eventos 
diferentes cadastrados, nesse caso usaremos o usuario eliel senha 12345
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import pyperclip
import time
import os

# setup inicial
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
os.environ['PATH'] += os.pathsep + diretorio_atual
browser = webdriver.Chrome()
browser.get('http://127.0.0.1:8000/usuarios/login/')
browser.maximize_window()
espera = WebDriverWait(browser, 10)

def fazer_login(usuario, senha):
    username = espera.until(EC.visibility_of_element_located((By.NAME, 'username')))
    password = espera.until(EC.visibility_of_element_located((By.NAME, 'senha')))
    btn_logar = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
    
    username.send_keys(usuario)
    password.send_keys(senha)
    time.sleep(2)
    btn_logar.click()
    
    
def test_pegar_link():  
    time.sleep(5)
    browser.get('http://127.0.0.1:8000/eventos/gerenciar_evento/')
    
    for evento in ['Django', 'Pytest', 'JS']:
        filtro_pesquisa = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'form-control')))
        btn_filtrar = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
        filtro_pesquisa.send_keys(evento)
        btn_filtrar.click()
        
        icone = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bi.bi-clipboard')))
        icone.click()
        alert = Alert(browser)
        time.sleep(3)
        alert.accept()

if __name__ == '__main__':
    fazer_login('eliel', '12345')
    test_pegar_link()  
    
    
    
    
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))

def fazer_login(usuario, senha):
    driver.get(login_url)
    username = wait_for_element(By.NAME, 'username')
    password = wait_for_element(By.NAME, 'senha')
    btn_logar = wait_for_element(By.CLASS_NAME, 'btn-principal')
    
    username.send_keys(usuario)
    password.send_keys(senha)
    btn_logar.click()

def test_pegar_link(eventos):
    driver.get(gerenciar_evento_url)
    
    for evento in eventos:
        filtro_pesquisa = wait_for_element(By.CLASS_NAME, 'form-control')
        btn_filtrar = wait_for_element(By.CLASS_NAME, 'btn-principal')
        filtro_pesquisa.send_keys(evento)
        btn_filtrar.click()
        
        icone = wait_for_element(By.CSS_SELECTOR, '.bi.bi-clipboard')
        icone.click()
        alert = Alert(driver)
        alert.accept()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    login_url = 'http://127.0.0.1:8000/usuarios/login/'
    gerenciar_evento_url = 'http://127.0.0.1:8000/eventos/gerenciar_evento/'
    
    fazer_login('eliel', '12345')
    eventos = ['Django', 'Pytest', 'JS']
    test_pegar_link(eventos)
    
    driver.quit()
   