from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.M023 import DemandeHistoriqueMesuresFines
from enedis.data_models.const import CadreAcces, SensMesure, TypeDonneesM023, FormatsM023
from enedis.services.commande_M023 import M023HistoriqueMesuresFines
import datetime as dt

def send_m023_demand():
    enedis_url = "ENEDIS_URL"
    login = "login"
    contract_id = "contract_id"
    path_public_cert = "path_public_cert"
    path_private_cert = "path_private_cert"

    # Récupération des variables d'env
    connection = EnedisConnection(enedis_url, login, contract_id, path_public_cert, path_private_cert)

    prms = ['00000000000001', '00000000000002']
    message = DemandeHistoriqueMesuresFines(dt.date(2024, 1, 1), dt.date(2024, 1, 31),
                                            CadreAcces.ACCORD_CLIENT,
                                            SensMesure.SOUTIRAGE,
                                            TypeDonneesM023.CDC,
                                            prms,
                                            FormatsM023.JSON)

    msg_sent, response = M023HistoriqueMesuresFines.m023(connection, message)
