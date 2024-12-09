import logging
from typing import Tuple

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.commandeaccesdonneesmesures import DemandeAccesDonneesMesures
from utils.regex import verification_prm

logger = logging.getLogger(__name__)

class CommandeAccesDonneesMesures:
    ns = 'http://www.enedis.fr/sge/b2b/commanderaccesdonneesmesures/v1.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/commandeaccesdonneesmesures/v1.0'
    name = 'CommanderAccesDonneesMesures-V1.0'
    port_binding = 'CommanderAccesDonneesMesuresBinding'
    service_path = 'CommanderAccesDonneesMesures/v1.0'

    @staticmethod
    def _create_xml_message(donnees: DemandeAccesDonneesMesures, client, service):

        xml = client.create_message(service, 'commanderAccesDonneesMesures', demande=donnees)
        return xml

    @classmethod
    def commande_acces_donnees_mesures(cls, connection: EnedisConnection, donnees: DemandeAccesDonneesMesures, send=True) -> Tuple[dict, dict]:
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)
            verification_prm(donnees['donneesGenerales']['pointId'])

            donnees['donneesGenerales']['initiateurLogin'] = connection.login
            donnees['donneesGenerales']['contrat']['contratId'] = connection.contract_id

            message = factory.CommanderAccesDonneesMesuresType(donnees)

            if send:
                response = serialize_object(service.commanderAccesDonneesMesures(message), dict)
            return serialize_object(message), response
        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}

