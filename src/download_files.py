import requests
from bs4 import BeautifulSoup
import os, time, json

def navega_pastas(url_cnpj: str) -> list:
    """
    Recebe uma URL da pasta principal da receita federal.

    Função que irá capturar o link das pastas, para download.
    """
    requisicao = requests.get(url_cnpj)
    time.sleep(3)
    soup = BeautifulSoup(requisicao.text, "html.parser")
    links = []

    for link in soup.find_all("a"):
        file = link.get("href")
        if file.endswith("/"):
            full = url_cnpj + file
            links.append(full)
    
    return links

def captura_links(url_cnpj: str) -> list:
    """
    Recebe uma URL da pasta da receita federal.

    Função que irá capturar o link dos arquivos, para download.
    """
    requisicao = requests.get(url_cnpj)
    time.sleep(3)
    soup = BeautifulSoup(requisicao.text, "html.parser")
    links = []

    for link in soup.find_all("a"):
        file = link.get("href")
        if file.endswith(".zip"):
            full = url_cnpj + file
            links.append(full)
    
    return links

def download(file_urls: list, root_dir: str, month_folder: str):
    """
    Faz o download de uma lista de arquivos a partir de URLs e os salva em uma pasta específica.
    
    Parâmetros:
    - file_urls (list): Lista de URLs dos arquivos a serem baixados.
    - root_dir (str): Diretório base onde os arquivos serão armazenados.
    - month_folder (str): Nome da pasta do mês onde os arquivos serão organizados.

    O script verifica se um arquivo já existe antes de baixá-lo. Caso o arquivo já esteja presente, 
    ele apenas registra essa informação no log e pula para o próximo. Se o download for bem-sucedido, 
    o arquivo é salvo e sua informação é registrada em um log JSON.

    O tempo de execução de cada download e o tempo total da operação são exibidos no console.
    """
    
    start_time = time.time()  # Marca o tempo inicial

    download_log_path = "/home/matz/Documentos/Projetos/OpenCNPJ/files/dados_baixados.json"
    target_folder = os.path.join(root_dir, month_folder)  
    os.makedirs(target_folder, exist_ok=True)  # Garante que o diretório existe

    for url in file_urls:
        file_start_time = time.time()

        file_name = os.path.basename(url)  
        file_path = os.path.join(target_folder, file_name)

        # Se o arquivo já existe, registra e pula
        if os.path.exists(file_path):
            print(f"Arquivo já existe: {file_path}. Pulando o download.")
            with open(download_log_path, "a") as log_file:
                json.dump({"folder_nm": target_folder, "file_nm": file_name}, log_file)
                log_file.write("\n")
            continue

        # Tenta baixar o arquivo
        print(f"Baixando {file_name}...")
        try:
            response = requests.get(url, timeout=30)  
            response.raise_for_status()  # Garante que o request foi bem-sucedido
        except requests.RequestException as e:
            print(f"Erro ao baixar {file_name}: {e}")
            continue  # Passa para o próximo arquivo

        # Salva o arquivo baixado
        with open(file_path, "wb") as file:
            file.write(response.content)
            print(f"Arquivo baixado: {file_name}")

        # Registra no log
        with open(download_log_path, "a") as log_file:
            json.dump({"folder_nm": target_folder, "file_nm": file_name}, log_file)
            log_file.write("\n")

        print(f"{time.time() - file_start_time:.2f} segundos para baixar {file_name}")

    print(f"Tempo total: {time.time() - start_time:.2f} segundos")