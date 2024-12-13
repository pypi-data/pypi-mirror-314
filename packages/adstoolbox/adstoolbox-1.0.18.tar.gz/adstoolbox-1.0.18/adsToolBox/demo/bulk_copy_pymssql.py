from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql

logger = Logger(Logger.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

source = dbMssql({
    'database': env.MSSQL_DWH_DB,
    'user': env.MSSQL_DWH_USER,
    'password': env.MSSQL_DWH_PWD,
    'port': env.MSSQL_DWH_PORT,
    'host': env.MSSQL_DWH_HOST
}, logger)
source.connect()
logger.set_connection(source, Logger.DEBUG)

source.sqlExec('''
IF OBJECT_ID('dbo.insert_test', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test;
CREATE TABLE dbo.insert_test (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);''')

rows = [(f'Name {i}', f'email{i}@example.com') for i in range(50_000)]
result = source.insertBulk('dbo.insert_test', ['name', 'email'], rows)
print(result)