from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql
from adsToolBox.dbPgsql import dbPgsql

import logging

logger = Logger(None, logging.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source = dbMssql({
    'database': env.MSSQL_DWH_DB,
    'user': env.MSSQL_DWH_USER,
    'password': env.MSSQL_DWH_PWD,
    'port': env.MSSQL_DWH_PORT_VPN,
    'host': env.MSSQL_DWH_HOST_VPN
}, logger)

source.connect()

res = source.sqlScalaire("SELECT COUNT(*) FROM insert_test;")
print(res)

dict_pg = {'database': env.PG_DWH_DB
                          , 'user': env.PG_DWH_USER
                          , 'password': env.PG_DWH_PWD
                          , 'port': env.PG_DWH_PORT
                          , 'host': env.PG_DWH_HOST}

source = dbPgsql(dict_pg, logger)
print(source.connection)
source.connect()
print(source.connection)

res = source.sqlScalaire("SELECT COUNT(*) FROM insert_test;")

print(res)