from download_files import navega_pastas, captura_links, download
from utils import check_and_create_dir
from unzip import descompactar
import time
import os

def main():
    data_dir = './data'
    check_and_create_dir(data_dir)
    url =  "https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/"
    path = f"/home/{os.getlogin()}/Documentos/Projetos/OpenCNPJ/data"
    
    # Baixando arquivos
    lista_link = navega_pastas(url)

    for pasta in lista_link[1:]:
        links = captura_links(url_cnpj= pasta)
        mes = pasta.split("/")[5]
        download(links, path, mes)

    # Descompactando

    descompactar(data_dir)


if __name__ == "__main__":
    main()