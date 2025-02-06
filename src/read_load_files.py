import pandas as pd
import psycopg2 as db

conn = db.connect(database= "cnpj_db", user="user", password="password")