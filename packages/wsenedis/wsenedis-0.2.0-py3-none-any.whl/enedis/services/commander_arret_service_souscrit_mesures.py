import logging
from typing import Tuple

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.commanderarretservicesouscritmesures import DemandeArretServiceSouscritMesures

logger = logging.getLogger(__name__)

class CommanderArretServiceSouscritMesures:
    ns = 'http://www.enedis.fr/sge/b2b/commanderarretservicesouscritmesures/v1.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/commandearretservicesouscritmesures/v1.0'
    name = 'CommandeArretServiceSouscritMesures-v1.0'
    port_binding = 'CommandeArretServiceSouscritMesuresBinding'
    service_path = 'CommandeArretServiceSouscritMesures/v1.0'

    @classmethod
    def commander_arret_service_souscrit_mesures(cls, connection: EnedisConnection, donnees: DemandeArretServiceSouscritMesures, send=True) -> Tuple[dict, dict]:
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            donnees['donneesGenerales']['initiateurLogin'] = connection.login
            donnees['donneesGenerales']['contratId'] = connection.contract_id

            message = factory.CommanderArretServiceSouscritMesuresType(donnees)

            if send:
                response = serialize_object(service.commanderArretServiceSouscritMesures(message), dict)

            return serialize_object(message, dict), response

        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}
