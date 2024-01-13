import subprocess
import os

def executar_scripts():
    # Lista dos scripts a serem executados
    scripts = [
        'test_eventos_novo_evento.py',
    ]

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    for script in scripts:
        script_path = os.path.join(diretorio_atual, script)  # Caminho absoluto para o script
        subprocess.run(['python', script_path], check=True)


if __name__ == '__main__':
    executar_scripts()
