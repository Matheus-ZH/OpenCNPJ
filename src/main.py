from download_files import navega_pastas, captura_links, download
from utils import check_and_create_dir
from unzip import descompactar
import time
import os

def main():
    data_dir = './data' # raw_data | data
    check_and_create_dir(data_dir)
    url =  "https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/"
    root_dir = f"/home/{os.getlogin()}/Documentos/Projetos/OpenCNPJ/data"
    
    # Baixando arquivos
    url_folder = navega_pastas(url)

    for folder in url_folder[1:]:
        file_urls = captura_links(url_cnpj= folder)
        month_folder = folder.split("/")[5]
        download(file_urls, root_dir, month_folder)

    # Descompactando

    # descompactar(data_dir)

if __name__ == "__main__":
    main()