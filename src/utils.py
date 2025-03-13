import os
import json

def check_and_create_dir(directory: str) -> None:
    '''
    Função para verificar se o diretorio já existe,
    se não cria um para assim começar o processo de download.
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(f"Diretório {directory} já existe.")


def check_files_exists(file: json) -> bool:
    pass