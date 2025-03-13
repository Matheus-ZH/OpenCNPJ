import pandas as pd
import psycopg2 as db
import os, sys

#conn = db.connect(database= "cnpj_db", user="user", password="password")
def connection():
    '''
    Conecta ao banco de dados
    '''  
    conn = None
    try:
        print("Conectando...")
        conn = db.connect(
                            #database= "cnpj_db", user="user", password="password", host="localhost", port="5432"
                            database=os.environ["DB_NAME"],
                            user=os.environ["DB_USERNAME"],
                            password=os.environ["DB_PASSWORD"],
                            host=os.environ["DB_HOST"],
                            port=os.environ["DB_PATH"]
                            )
    except (Exception, db.DatabaseError) as error:       
        print(error)
        sys.exit(1)
    
    print("Tudo certo, Conexão realizada!")
    return conn

con = connection()

def read_files(dir: str) -> pd.DataFrame:
    '''
    Recebe um caminho de diretorio, lê os arquivos listados.
    '''
    try:
        for i in os.listdir(dir):
            path = os.path.join(dir, i)
            df = pd.read_csv(path, sep=";")
    except Exception as e:
        return e
    
    return df

def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    trata os dados de forma básica e ajusta o nome das colunas
    '''
    return df

def load_db(con: db.connect) -> None:
    '''
    Carregar dados no banco na primeira camada.
    '''
    cur = con.cursor()
    cur.execute()

cur = con.cursor()
cur.execute(query='''
    CREATE TABLE leads (id INTEGER PRIMARY KEY, name VARCHAR);
            ''')

cur.execute('''
SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
            ''')

b = cur.fetchall()
print(b)

cur.execute('''
            INSERT INTO leads (id, name)
            VALUES (2, 'ZAMPOLLI')
            ''')

cur.execute('''
            SELECT
                *
            FROM leads
            ''')

a = cur.fetchall()
print(a)