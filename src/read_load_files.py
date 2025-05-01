import pandas as pd
import psycopg2 as db
import os, sys, glob, json
from sqlalchemy import create_engine, Engine, MetaData, Table, Column, Integer, BigInteger, String, Text, Date, Numeric, DateTime, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.types import TypeEngine
from typing import Dict, List, Union, Optional
from utils import formatar_tempo, medir_tempo

# Mapeamento de tipos string para tipos SQLAlchemy
TYPE_MAPPING = {
    "Integer": Integer,
    "String": String,
    "Text": Text,
    "Date": Date,
    "Numeric": Numeric,
    "BigInteger": BigInteger
    # Adicione outros tipos conforme necessário
}

engine = create_engine(
    f'postgresql+psycopg2://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PATH"]}/{os.environ["DB_NAME"]}'
)

metadata = MetaData()

def criar_tabela(
    engine: Engine,
    schema: str,
    table_name: str,
    columns: Dict[str, Dict[str, Union[TypeEngine, dict]]],
    if_exists: str = 'fail',
    table_comment: Optional[str] = None
) -> Table:
    """
    Cria uma tabela no banco de dados com configurações avançadas.
    
    Parâmetros:
    -----------
    engine : Connect()
        conexão com o banco (ex: 'postgresql://user:pass@localhost:5432/db')
    schema : str
        Nome do schema onde a tabela será criada
    table_name : str
        Nome da tabela a ser criada
    columns : Dict[str, Dict]
        Dicionário de colunas com metadados avançados. Formato:
        {
            'nome_coluna': {
                'type': TipoSQLAlchemy,  # obrigatório (ex: Integer, String(50))
                'primary_key': bool,      # opcional
                'foreign_key': str,       # opcional (ex: 'schema.tabela.coluna')
                'index': bool,            # opcional
                'nullable': bool,        # opcional (padrão True)
                'unique': bool,          # opcional
                'comment': str,           # opcional
                'default': valor          # opcional
            }
        }
    if_exists : str
        Comportamento se tabela existir ('fail', 'replace' ou 'append')
    table_comment : str, optional
        Comentário descritivo da tabela
    """
    
    metadata = MetaData()
    
    if if_exists == 'fail' and engine.has_table(table_name):
        raise ValueError(f"Tabela {schema}.{table_name} já existe!")
    
    sqlalchemy_columns = []
    constraints = []
    
    for col_name, col_config in columns.items():
        if 'type' not in col_config:
            raise ValueError(f"Configuração 'type' faltando para a coluna {col_name}")
        
        # Argumentos básicos da coluna
        col_args = {
            'nullable': col_config.get('nullable', True),
            'comment': col_config.get('comment'),
            'index': col_config.get('index', False),
            'unique': col_config.get('unique', False)
        }
        
        # Default value
        if 'default' in col_config:
            col_args['server_default'] = str(col_config['default'])
        
        # Cria a coluna
        col = Column(col_name, col_config['type'], **col_args)
        
        # Adiciona FK se especificado
        if 'foreign_key' in col_config:
            fk_parts = col_config['foreign_key'].split('.')
            if len(fk_parts) == 3:
                fk_schema, fk_table, fk_column = fk_parts
                col.append_foreign_key(f"{fk_schema}.{fk_table}({fk_column})")
            else:
                col.append_foreign_key(col_config['foreign_key'])
        
        sqlalchemy_columns.append(col)
        
        # Marca PK para adicionar depois
        if col_config.get('primary_key', False):
            constraints.append(PrimaryKeyConstraint(col_name))
    
    # Cria a tabela com todas as colunas e constraints
    table = Table(
        table_name,
        metadata,
        *sqlalchemy_columns,
        *constraints,
        comment=table_comment
    )
    
    metadata.create_all(engine)
    print(f"Tabela {schema}.{table_name} criada com sucesso!")

def criar_tabela_com_json(
        engine: Engine,
        schema: str,
        table_name: str,
        json_path: str,
        if_exists: str = 'fail'
) -> Table:
    """
    Cria uma tabela no banco de dados com configurações avançadas.
    
    Parâmetros:
    -----------
    engine : Connect()
        conexão com o banco (ex: 'postgresql://user:pass@localhost:5432/db')
    schema : str
        Nome do schema onde a tabela será criada
    table_name : str
        Nome da tabela a ser criada
    json_path : str
        String com o caminho do arquivo json que armazena as informações para criação das tabelas.
    if_exists : str
        Comportamento se tabela existir ('fail', 'replace' ou 'append')
    """
    # Carrega o JSON
    with open(json_path, "r") as f:
        table_schemas = json.load(f)
    
    # Obtém o schema da tabela específica
    table_schema = table_schemas.get(table_name)
    if not table_schema:
        raise ValueError(f"Tabela {table_name} não encontrada no JSON")
    
    # Converte os tipos de string para objetos SQLAlchemy
    columns = {}
    for col_name, col_config in table_schema.items():
        # Faz uma cópia do dicionário para não modificar o original
        col_config = col_config.copy()
        
        # Processa o tipo
        type_str = col_config.pop("type")
        
        # Para tipos com parâmetros (como String(150))
        if "(" in type_str:
            type_name, params = type_str.split("(", 1)
            params = params.rstrip(")").split(",")
            type_class = TYPE_MAPPING[type_name]
            if len(params) == 1:
                col_type = type_class(int(params[0]))
            else:
                col_type = type_class(*map(int, params))
        else:
            col_type = TYPE_MAPPING[type_str]
        
        columns[col_name] = {"type": col_type, **col_config}
    
    # Chama a função que cria a tabela no banco de dados
    criar_tabela(
        engine=engine,
        schema=schema,
        table_name=table_name,
        columns=columns,
        if_exists=if_exists
    )

def criar_todas_tabelas(
        engine: Engine,
        schema: str,
        json_path: str,
        if_exists: str = 'replace'
) -> Table:
    """
    Cria uma tabela no banco de dados com configurações avançadas.
    
    Parâmetros:
    -----------
    engine : Connect()
        conexão com o banco (ex: 'postgresql://user:pass@localhost:5432/db').
    schema : str
        Nome do schema onde a tabela será criada.
    json_path : str
        String com o caminho do arquivo json que armazena as informações para criação das tabelas.
    if_exists : str
        Replace pois sempre iremos recriar todas as tabelas ao chamar essa função.
    """
    with open(json_path) as f:
        all_schemas = json.load(f)
    
    for table_name in all_schemas:
        criar_tabela_com_json(
            engine=engine,
            schema=schema,
            table_name=table_name,
            json_path=json_path,
            if_exists=if_exists
        )

@medir_tempo
def copy_to_postgre(
    engine: Engine,
    dir: str, 
    table_name: str
) -> None:
    """
    Recebe caminho de um diretorio e carrega os dados para o banco de Dados,
    realizando o equivalente a um bulk insert.


    """
    con = engine.connect().connection
    cursor = con.cursor()

    prim_arq = os.listdir(dir)[0]
    df = pd.read_csv(os.path.join(dir, prim_arq), sep=';', header=None, encoding='latin-1')
    df = df.astype('str')
    df[:0].to_sql(name= table_name, con= engine, if_exists="append", method="multi", index=False)

    copy_from = f"""
            COPY "{table_name}" 
            FROM STDIN
            WITH (
                FORMAT CSV,
                DELIMITER ';',
                HEADER false
            );
            """
    for arq in os.listdir(dir):
        file_path = os.path.join(dir, arq)
        with open(file_path, encoding='latin-1') as f:
            cursor.copy_expert(copy_from, file= f)
        print(f"Processed file: {arq}")
        
    con.commit()
    cursor.close()
    con.close()
    return None

def read_files_and_load_chunks(
    dir: str,
    header: int | None,
    colnames: list[str] | None,
    name_tb: str
) -> None:
    '''
    Recebe um caminho de diretorio, lê os arquivos listados e insere eles em pedaçõs no banco.
    '''
    try:
        for i in os.listdir(dir):
            path = os.path.join(dir, i)
            for chunk in pd.read_csv(path, sep=";", names=colnames, header=header, encoding='latin-1', index_col=None, na_values='NULL', chunksize=50000):
                chunk.to_sql(name= name_tb, con= engine, if_exists="append", method="multi")
            return print("Dados enviados para a tabela: {}".format(name_tb))
    except Exception as e:
        return print("Erro {} ao enviar os dados para a tabela: {}".format(e, name_tb))
    
    return None

# EXEMPLO DE USO
criar_tabela(
        engine,
        schema="tables",
        table_name="BRONZE_CNAES",
        columns="TESTE",
        if_exists="replace",
        table_comment="Tabela de clientes com metadados avançados"
    )

criar_tabela_com_json(
        engine,
        schema="tables",
        table_name="CNAES",
        json_path="/home/matz/Documentos/Projetos/OpenCNPJ/files/table_data_types_bronze.json",
        if_exists="replace"
)

criar_todas_tabelas(engine, "tables", "/home/matz/Documentos/Projetos/OpenCNPJ/files/table_data_types_bronze.json")

# DEU XABU PELO SCHEMA PRIMEIRO ISSO DEVE DAR PARA AJUSTAR
# DEPOIS XABU PELO CAMPO NUMERIC N ACEITAR , 1000,00 E SIM . 1000.00
# possiveis soluções: 
    # 1 -> atualizar o banco para um postgresql mais recente
    # 2 -> Ler e tratar o campo o que deixa mais pesado...
        # Num ambiente que já existe o ideal séria tratar..
        # Como eu posso mudar a tempo acho que o mais produtivo é tentar atualizar... e Verificar se DECIMAL ',' vai.
        # Ou processar isso no banco de dados com o DBT nas próximas camadas bronze, silver, gold

# EXEMPLO DE USO
df_estudo_cnaes = read_files_and_load_chunks("/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Cnaes", None, ['ID_ACTIVITY', 'ACTIVITY_DESC'],"BRONZE_CNAES")
df_estudo_empresas = read_files_and_load_chunks("/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Empresas", None, None,"BRONZE_EMPRESAS")
df_estudo_socios = copy_to_postgre(engine, "/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Socios","BRONZE_SOCIOS")
copy_to_postgre(engine, "/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Cnaes","BRONZE_CNAES")
copy_to_postgre(engine, "/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Empresas","BRONZE_EMPRESAS")
copy_to_postgre(engine, "/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Estabelecimentos","BRONZE_ESTABELECIMENTOS")
copy_to_postgre(engine, "/home/matz/Documentos/Projetos/OpenCNPJ/data/2023-05/Socios","BRONZE_SOCIOS")
