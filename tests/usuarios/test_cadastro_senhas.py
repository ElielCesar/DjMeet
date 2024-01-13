from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# caminho para o webdriver e setup inicial
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
os.environ['PATH'] += os.pathsep + diretorio_atual
browser = webdriver.Chrome()
browser.get('http://127.0.0.1:8000/usuarios/cadastro/')
browser.maximize_window()

# datasets para validar senhas
dataset = [
    ('1','1'),
    ('',''),
    ('12','123'),
    ('  ','  '),
    (' ','  '),
    ('123 ','123 '),
    (True, True),
]

def test_validar_senha():
    # tempo para voce reduzir o zoom da página
    time.sleep(5)
    espera = WebDriverWait(browser, 10)
    

    for valor_senha, valor_conf_senha in dataset:
        nome_completo = espera.until(EC.visibility_of_element_located((By.NAME, 'nome_completo')))
        username = espera.until(EC.visibility_of_element_located((By.NAME, 'username')))
        email = espera.until(EC.visibility_of_element_located((By.NAME, 'email')))
        telefone = espera.until(EC.visibility_of_element_located((By.NAME, 'telefone')))
        cidade = espera.until(EC.visibility_of_element_located((By.NAME, 'cidade')))
        senha = espera.until(EC.visibility_of_element_located((By.NAME, 'senha')))
        confirmar_senha = espera.until(EC.visibility_of_element_located((By.NAME, 'confirmar_senha')))
        btn_cadastrar = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))
        
        nome_completo.send_keys('Andrey Alencar')
        username.send_keys('andrey')
        email.send_keys('andrey@gmail.com')
        telefone.send_keys('69 99292-2212')
        cidade.send_keys('Ariquemes')
        estado = Select(browser.find_element(By.ID, 'estado'))
        estado.select_by_visible_text('Rondônia')

        senha.send_keys(valor_senha)
        confirmar_senha.send_keys(valor_conf_senha)
        btn_cadastrar.click()
        time.sleep(2)

        browser.refresh()

    print('Teste test_validar_senha() executado com sucesso!')

if __name__ == '__main__':
    test_validar_senha()
