from timer import timer
from logger import Logger
import polars as pl

class dataComparator:
    def __init__(self, dictionnary: dict, logger: Logger):
        """
        Initialise un dataComparator avec les informations de connexions aux bases de données
        :param dictionnary: le dictionnaire qui contient les informations du pipeline
            - 'db_source_1': la base de données source 1
            - 'query_source_1': la requête à envoyer à la source 1
            - 'db_source_2': la base de données source 2
            - 'query_source_2': la requête à envoyer à la source 2
            - 'batch_size': la taille des lots pour le traitement en batch
        :param logger: le logger pour gérer la journalisation des évènements du pipeline
        """
        self.logger = logger
        self.__db_source_1 = dictionnary.get('db_source_1')
        self.__query_source_1 = dictionnary.get('query_source_1')
        self.__db_source_2 = dictionnary.get('db_source_2')
        self.__query_source_2 = dictionnary.get('query_source_2')
        self.__batch_size = dictionnary.get('batch_size', 10_000)

    def _fetch_data(self, db, query):
        """
        Exécute la requête donnée sur la base spécifiée et retourne un DataFrame Polars
        :param db: la base sur laquelle envoyer la requête
        :param query: la requête à envoyer
        :return: le résultat de la requête sous forme de DataFrame
        """
        self.logger.info(f"Exécution de la requête sur {db.get('name', 'bdd')}")
        db['db'].connect()
        data = list(db.sqlQuery(query))
        return pl.DataFrame(data, orient='row', strict=False)

    @timer
    def compare(self):
        """
        Compare les résultats des deux requêtes SQL entre les deux bases de données.
        :return: Un dictionnaire contenant les différences si elles existent
        """
        try:
            data_1 = self._fetch_data(self.__db_source_1, self.__query_source_1)
            data_2 = self._fetch_data(self.__db_source_2, self.__query_source_2)
            if data_1.equals(data_2):
                self.logger.info("Les deux résultats des requêtes sont identiques.")
                return {"status": "identical", "differences": None}
            else:
                diff_1_to_2 = data_1.filter(~data_1.is_in(data_2))
                diff_2_to_1 = data_2.filter(~data_2.is_in(data_1))
                differences = {
                    "only_in_source_1": diff_1_to_2.rows(),
                    "only_in_source_2": diff_2_to_1.rows()
                }
                self.logger.warning("Les résultats des deux requêtes sont différents.")
                return {"status": "different", "differences": differences}
        except Exception as e:
            self.logger.error(f"Erreur lors de la comparaison des données: {e}")
            raise
