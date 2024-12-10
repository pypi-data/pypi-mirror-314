from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql
from adsToolBox.dbPgsql import dbPgsql

from adsToolBox.global_config import set_timer

set_timer(True)
logger = Logger(Logger.DEBUG, "EnvLogger")
env = env(logger,
          'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

"""
source = dbPgsql({'database':env.PG_DWH_DB
                    , 'user':env.PG_DWH_USER
                    , 'password':env.PG_DWH_PWD
                    , 'port':env.PG_DWH_PORT
                    , 'host':env.PG_DWH_HOST}, logger)
source.connect()
logger.set_connection(source, Logger.DEBUG)

source.sqlExec('''DROP TABLE IF EXISTS insert_test;''')
source.sqlExec('''
CREATE TABLE IF NOT EXISTS insert_test (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);
''')
"""

source = dbMssql({
    'database': env.MSSQL_DWH_DB,
    'user': env.MSSQL_DWH_USER,
    'password': env.MSSQL_DWH_PWD,
    'port': env.MSSQL_DWH_PORT_VPN,
    'host': env.MSSQL_DWH_HOST_VPN
}, logger)
source.connect()
logger.set_connection(source, Logger.DEBUG)

#logger.create_logs_tables()
source.sqlExec('''
IF OBJECT_ID('dbo.insert_test', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test;
''')
source.sqlExec('''
CREATE TABLE dbo.insert_test (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);''')

logger.info("Message d'info")
logger.debug("Message de debug")
logger.warning("Message de warning")
logger.error("Message d'erreur")
logger.custom_log(25, "Message custom")

source.insert('insert_test', ['name', 'email'], ['ERR', 'MAIL'])

res = source.sqlScalaire("SELECT COUNT(*) FROM insert_test;")

print(res)

logger.log_close("Réussite", "Tout le script a fonctionné")

logger.info("Cela ne devrait pas s'afficher.")
