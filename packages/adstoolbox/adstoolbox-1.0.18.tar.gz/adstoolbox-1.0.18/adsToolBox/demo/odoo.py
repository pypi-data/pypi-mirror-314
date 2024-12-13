from adsToolBox import dbPgsql
from odoo import OdooConnector
from adsToolBox.logger import Logger
from adsToolBox.loadEnv import env

import logging

logger = Logger(None, logging.DEBUG, "EnvLogger")
env = env(logger, '.env')

logger_connection = dbPgsql({'database': env.PG_DWH_DB,
                             'user': env.PG_DWH_USER,
                             'password': env.PG_DWH_PWD,
                             'port': env.PG_DWH_PORT,
                             'host': env.PG_DWH_HOST},
                            None)

source = OdooConnector({'url': '', 'db': '', 'username': '', 'password': ''}, logger)

source.connect()

domain = [('', '=', True)]
partner_ids = source.search_records('res.partner', domain)

logger.info(f"Found partner IDs: {partner_ids}")

if partner_ids:
    partners = source.read_records('', partner_ids, [''])
    logger.info(f"Partner details: {partners}")