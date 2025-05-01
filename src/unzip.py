import zipfile
import os, re

def descompactar(
        path: str
    ) -> None:
    """
    Recebe um caminho da pasta que estará os arquivos baixados.
    E descompacta todos os arquivos zip e após isso deleta o arquivo zip,
    restando apenas o arquivo que havia dentro.
    """
    diretorio = os.listdir(path)
    for pasta in diretorio:
        mes = os.path.join(path, pasta)
        for base_dados in os.listdir(mes):
            try:
                if base_dados.endswith('.zip'):
                    full_path = os.path.join(mes, base_dados)
                    with zipfile.ZipFile(full_path, 'r') as zip:
                        name_folder = re.match(r"\D+", base_dados.split('.')[0])
                        path_new_folder = os.path.join(mes, name_folder.group(0))
                        if os.path.exists(path_new_folder):
                            zip.extractall(path_new_folder)
                        else:    
                            os.mkdir(path_new_folder)
                            zip.extractall(path_new_folder)
                    os.remove(full_path)
            except Exception as exc:
                print(f"Erro {type(exc)} ao Descompactar a pasta: {full_path}")
                continue

    """
    Cenários - Realizei o download de 60gb de arquivos zipados.
        1 - Salvo os arquivos numa pasta / bucket: 60gb
            Descompacto todos eles e salvo em outra pasta / bucket: 60gb
            Leio os arquivos descompactados: 60gb

        2 - Salvo os arquivos numa pasta / bucket: 60gb
            Descompacto todos eles e salvo em outra pasta, apago o arquivo zip
            Leio os arquivos descompactados
    """