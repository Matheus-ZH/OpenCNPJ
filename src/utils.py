import os

def check_and_create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(f"Diretório {directory} já existe.")

