from adsToolBox import pipeline
from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql
from adsToolBox.dbPgsql import dbPgsql

logger = Logger(Logger.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

rows = [(f'Name {i}', f'email{i}@example.com', i) for i in range(50_000)]

source_mssql = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT,
                      'host': env.MSSQL_DWH_HOST}, logger)
source_mssql.connect()

logger.set_connection(source_mssql, logger.INFO)
source_mssql.sqlExec('''
IF OBJECT_ID('dbo.insert_test', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test;
CREATE TABLE dbo.insert_test (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    age INT
);
''')

destination = {
    'name': 'test',
    'db': source_mssql,
    'table': 'insert_test',
    'cols': ['name', 'email', 'age']
}
rows[12121] = ('Name', 'Mail', 'Age')

pipe = pipeline({
    'tableau': rows,
    'db_destination': destination,
    'batch_size': 5_000
}, logger)
res = pipe.run()
print(res)

logger.log_close("Success", "Test nouveaux pipelines réussis.")