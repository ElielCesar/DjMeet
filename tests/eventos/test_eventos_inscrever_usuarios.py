'''
Esperado: Inscrever 3 usuários Teste1, Teste2 e Teste3 em um evento.
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

# urls do sistema
url_login = 'http://127.0.0.1:8000/usuarios/login/'
url_logout = 'http://127.0.0.1:8000/usuarios/logout'
meus_eventos = 'http://127.0.0.1:8000/eventos/meus_eventos'
url_evento = 'http://127.0.0.1:8000/eventos/inscrever_evento'
url_participantes = 'http://127.0.0.1:8000/eventos/participantes_evento'

def fazer_login(usuario, senha):
    wait = WebDriverWait(browser, 10)
    
    username = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
    password = wait.until(EC.visibility_of_element_located((By.NAME, 'senha')))
    btn_logar = browser.find_element(By.CLASS_NAME, 'btn-principal')
        
    username.send_keys(usuario)
    password.send_keys(senha)
    btn_logar.click()


def test_inscrever_no_evento(id_evento):
    time.sleep(3)
    espera = WebDriverWait(browser, 10)
    dados_login = [('teste1', '12345'), ('teste2', '12345'), ('teste3', '12345'), ]
    
    for user, senha in dados_login:
        fazer_login(user, senha)
        browser.get(f'{url_evento}/{id_evento}/') 
     
        btn_inscrever = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
        btn_inscrever.click()
        time.sleep(3)
    
        browser.get(meus_eventos)
        
        try:
            espera.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-outline-primary')))
        except:
            print("O botão não existe ou não é visível.")
                
        browser.get(url_logout)
    

def test_validar_inscritos(evento_id):
    browser.get(f'{url_participantes}/{evento_id}')
    time.sleep(7) # tempo para reduzir o zoom da página
    espera = WebDriverWait(browser, 10)
    
    for inscrito in ['teste1', 'teste2', 'teste3']:
        assert inscrito in browser.page_source, f'Usuário esperado não foi inscrito!!'
        
    btn_exportar_csv = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
    btn_exportar_csv.click()
    time.sleep(5)
    browser.get(url_logout)
    
    print('O teste inscrever_usuarios() foi executado com sucesso!')
        


if __name__ == '__main__':
    # aqui inscreve os 3 usuários - caso já tenha inscrito, apenas comente
    test_inscrever_no_evento(14)
    
    # aqui valida se realmente foram inscritos - esse user tem de ser o dono do evento
    fazer_login('eliel', '12345')
    test_validar_inscritos(14)

