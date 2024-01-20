'''
Esperado: Criar 3 usuarios com sucesso pela página de cadastro.
Todos os 3 usuários devem ser cadastrados, mas ao tentar cadastrar os mesmos usuarios
o teste deve falhar!
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


# dataset para o teste
dataset1 = [
    ('Teste1', 'teste1'),
    ('Teste2', 'teste2'),
    ('Teste3', 'teste3'),
]


def test_criar_3_usuarios(mensagem_esperada, css_seletor):
    # tempo para voce reduzir o zoom da página
    time.sleep(5)
    espera = WebDriverWait(browser, 10)
    
    for nome, usuario in dataset1:
        # elementos do formulário
        nome_completo = espera.until(EC.visibility_of_element_located((By.NAME, 'nome_completo')))
        username = espera.until(EC.visibility_of_element_located((By.NAME, 'username')))
        email = espera.until(EC.visibility_of_element_located((By.NAME, 'email')))
        telefone = espera.until(EC.visibility_of_element_located((By.NAME, 'telefone')))
        cidade = espera.until(EC.visibility_of_element_located((By.NAME, 'cidade')))
        senha = espera.until(EC.visibility_of_element_located((By.NAME, 'senha')))
        confirmar_senha = espera.until(EC.visibility_of_element_located((By.NAME, 'confirmar_senha')))
        btn_cadastrar = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-principal')))

        # valores para os campos
        nome_completo.send_keys(nome)
        username.send_keys(usuario)
        email.send_keys('teste@gmail.com')
        cidade.send_keys('Jaru')
        telefone.send_keys('6999292-1212')
        estado = Select(browser.find_element(By.ID, 'estado'))
        estado.select_by_visible_text('Rondônia')
        senha.send_keys('12345')
        confirmar_senha.send_keys('12345')

        btn_cadastrar.click()
        time.sleep(2)

        mensagem = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_seletor)))
        assert mensagem_esperada in mensagem.text, 'Mensagem incorreta, o teste falhou!'
        browser.refresh()

    print('Teste test_criar_3_usuarios() executado!')

if __name__ == '__main__':
    test_criar_3_usuarios('Usuário criado com sucesso!', '.alert.alert-success')
    test_criar_3_usuarios('Um usuário com esse username já existe!', '.alert.alert-warning')
