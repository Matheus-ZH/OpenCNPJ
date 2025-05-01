import os
import json
import time

def check_and_create_dir(
        directory: str
    ) -> None:
    '''
    Função para verificar se o diretorio já existe,
    se não cria um para assim começar o processo de download.
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(f"Diretório {directory} já existe.")


def check_files_exists(
        file: json
    ) -> bool:
    pass

def formatar_tempo(
        segundos: float
    ) -> str:
    horas = int(segundos // 3600)
    segundos %= 3600
    minutos = int(segundos // 60)
    segundos = int(segundos % 60)
    milissegundos = int((segundos - int(segundos)) * 1000)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}:{milissegundos:03d}"

def medir_tempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        tempo_execucao_segundos = fim - inicio
        tempo_formatado = formatar_tempo(tempo_execucao_segundos)
        print(f"A função '{func.__name__}' levou {tempo_formatado} para executar.")
        return resultado
    return wrapper