import requests
from bs4 import BeautifulSoup
import os, time

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

def download(links: list, path: str ,mes_arq: str):
    tmp_ini = time.time()
    
    for link in links[0:]:
        tmp_inicial_down = time.time()
        pasta_nova = os.path.join(path, mes_arq)
        if os.path.exists(pasta_nova):
            print(f"Arquivo já existe em {pasta_nova}. Pulando o download.")
            dict = {"folder_nm": pasta_nova,
                    "file_nm": link[link.rfind("/")+1:]}
            with open(f"files/dados_baixados.json", "w") as outfile:
                outfile.write(dict)
            return
        else:
            nome_arquivo = link[link.rfind("/")+1:]
            print(f"Realizando o Download do arquivo {nome_arquivo}")
            response = requests.get(link)
            time.sleep(3)
            if not os.path.exists(pasta_nova):
                try:
                    print("Criando diretorio..")
                    os.makedirs(pasta_nova)
                except OSError:
                    pass

            with open(f"data/{mes_arq}/{nome_arquivo}", "wb") as file:
                    file.write(response.content)
                    print(f"Arquivo baixado {nome_arquivo}")
                    tmp_final_down = time.time()
            
            dict = {"folder_nm": pasta_nova,
                    "file_nm": nome_arquivo}
            
            with open(f"files/dados_baixados.json", "w") as outfile:
                outfile.write(dict)

        print(f"{tmp_final_down - tmp_inicial_down} segundos")

    # descompactar(path)

    tmp_final = time.time()

    print(f"{tmp_final - tmp_ini} segundos")