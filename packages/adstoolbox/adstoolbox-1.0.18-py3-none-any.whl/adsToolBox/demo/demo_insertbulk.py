import logging
import time
from adsToolBox.loadEnv import env
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.logger import Logger

logger = Logger(None, logging.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

logger_connection = dbPgsql({'database': env.PG_DWH_DB
                          , 'user': env.PG_DWH_USER
                          , 'password': env.PG_DWH_PWD
                          , 'port': env.PG_DWH_PORT
                          , 'host': env.PG_DWH_HOST},
                      None)
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS",
                    "LOGS_details")
logger.disable()
fake = Faker()

def generate_data(n):
    data = []
    for _ in range(n):
        data.append((
            fake.name(),
            fake.email()
        ))
    return data

n = 50_000
rows = generate_data(n)
print(f"{n} lignes générées.")
columns = ['name', 'email']

def old_insert_bulk(db, table, cols, rows):
    start = time.time()
    print(db.insertBulk(table, cols=cols, rows=rows)[0])
    print(f"Ancienne méthode - Temps d'exécution: {time.time() - start} secondes")

def new_insert_bulk(db, table, cols, rows):
    start = time.time()
    print(db.insertBulk(table, cols=cols, rows=rows)[0:-1])
    print(f"Nouvelle méthode - Temps d'exécution: {time.time() - start} secondes")

source = dbPgsql({'database':env.PG_DWH_DB
                    , 'user':env.PG_DWH_USER
                    , 'password':env.PG_DWH_PWD
                    , 'port':env.PG_DWH_PORT
                    , 'host':env.PG_DWH_HOST}, logger)

source.connect()
source.sqlExec(''' DROP TABLE IF EXISTS insert_test; ''')
print("Table Supprimée")
source.sqlExec('''
CREATE TABLE IF NOT EXISTS insert_test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);''')
print("Table Recréée")

#old_insert_bulk(source, 'dbo.insert_test', columns, rows)

new_insert_bulk(source, 'insert_test', columns, rows)



