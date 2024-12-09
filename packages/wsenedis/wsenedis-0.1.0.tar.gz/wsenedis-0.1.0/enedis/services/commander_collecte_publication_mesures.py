import logging

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.commandercollectepublicationmesures import DemandeCollectePublicationMesure
from utils.regex import verification_prm

logger = logging.getLogger(__name__)

class CommanderCollectePublicationMesures:
    name = 'CommandeCollectePublicationMesures-v3.0'
    ns = 'http://www.enedis.fr/sge/b2b/commandercollectepublicationmesures/v3.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/commandecollectepublicationmesures/v3.0'
    port_binding = 'CommandeCollectePublicationMesuresBinding'
    service_path = 'CommandeCollectePublicationMesures/v3.0'

    @classmethod
    def commander_collecte_publication(cls, connection:EnedisConnection, donnees: DemandeCollectePublicationMesure, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            donnees['donneesGenerales']['initiateurLogin'] = connection.login
            donnees['donneesGenerales']['contratId'] = connection.contract_id

            message = factory.CommanderCollectePublicationMesuresType(donnees)
            if send:
                response = serialize_object(service.commanderCollectePublicationMesures(message), dict)

            return serialize_object(message, dict), response

        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}
