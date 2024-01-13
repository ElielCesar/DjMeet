''''
Esperado: Ao executar esse teste, todo os campos devem acusar erro
pois foram intencionalmente preenchidos com valores inválidos a cada
iteracao do for. 

O usuário não pode ser cadastrado, se for algo deu errado!
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

# datasets para testes
dataset2 = ['A', 'andrey', 'andrey@gmail.com','6999292-1212', 'Ariquemes', '1234', '1234']
dataset3 = ['Andrey Alencar', 'a', 'andrey@gmail.com','6999292-1212', 'Ariquemes', '1234', '1234']
dataset4 = ['Andrey Alencar', 'andrey', 'a@gmail','6999292-1212', 'Ariquemes', '1234', '1234']
dataset5 = ['Andrey Alencar', 'andrey','andrey@gmail.com', '69 92', 'Ariquemes', '1234', '1234']
dataset6 = ['Andrey Alencar', 'andrey', 'andrey@gmail.com','6999292-1212', 'Ari', '1234', '1234']


def test_tamanho_minimo():
    # tempo para voce reduzir o zoom da página
    time.sleep(5)
    espera = WebDriverWait(browser, 10)
    
    for dataset in [dataset2, dataset3, dataset4, dataset5, dataset6]:
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
            time.sleep(0.5)
            elemento.send_keys(dataset[i])
            i += 1

        estado = Select(browser.find_element(By.ID, 'estado'))
        estado.select_by_visible_text('Rondônia')
        btn_cadastrar.click()
        time.sleep(2)

        mensagem = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-warning')))
        assert 'O campo ' in mensagem.text, f"O texto não existe na mensagem!"
        
        browser.refresh()
        
    print('Teste test_tamanho_minimo() executado com sucesso!')

if __name__ == '__main__':
    test_tamanho_minimo()