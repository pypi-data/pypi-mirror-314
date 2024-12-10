import logging
from adsToolBox.loadEnv import env
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.dbMssql import dbMssql
from adsToolBox.pipeline import pipeline
from adsToolBox.logger import Logger
from adsToolBox.global_config import set_timer

logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source_pg = dbPgsql({'database':env.PG_DWH_DB
                    , 'user':env.PG_DWH_USER
                    , 'password':env.PG_DWH_PWD
                    , 'port':env.PG_DWH_PORT
                    , 'host':env.PG_DWH_HOST}, logger)
source_pg.connect()
source_mssql = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT,
                      'host': env.MSSQL_DWH_HOST}, logger)
source_mssql.connect()
set_timer(True)

destination = {
    'name': 'test',
    'db': source_mssql,
    'table': 'insert_test_2',
    'cols': [2, 3]
}

destination["db"].sqlExec('''
IF OBJECT_ID('dbo.insert_test_2', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test_2;

CREATE TABLE dbo.insert_test_2 (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);
''')

source = [(f'Name {i}', f'email{i}@example.com') for i in range(5)]

# Déclaration du pipeline
pipe = pipeline({
    'tableau': source, # La source du pipeline
    'db_destination': destination, # La destination du pipeline
    'mode': 'bulk', # en mode bulk, plus rapide
    'checkup': True, # Vérifie par la suite si la table destination
}, logger)

rejects = pipe.run()

logger.info("Fin de la démonstration")