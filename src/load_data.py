import pandas as pd
import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost:5432/cnpj_db')

conn = psycopg2.connect(host="localhost",
                        port="5432",
                        database="cnpj_db",
                        user="user",
                        password="password")
cur = conn.cursor()

def load_csv_db(path: str, table_name: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    
    return