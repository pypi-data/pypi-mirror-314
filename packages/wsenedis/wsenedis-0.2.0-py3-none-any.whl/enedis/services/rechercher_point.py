import logging
from pprint import pprint

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.recherchepoint import RechercherPoint

logger = logging.getLogger(__name__)


class RecherchePoint:
    ns = 'http://www.enedis.fr/sge/b2b/services/rechercherpoint/v2.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/services'
    name = 'RecherchePoint-v2.0'
    service_name = 'rechercherPoint'
    port_binding = 'RecherchePointBinding'
    service_path = 'RecherchePoint/v2.0'

    @classmethod
    def recherche_point(cls, connection: EnedisConnection, donnees: RechercherPoint, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)
            donnees['loginUtilisateur'] = connection.login
            message = factory.RechercherPointType(**donnees)

            if send:
                response = serialize_object(service.rechercherPoint(**{k:message[k] for k,v in donnees.items()}), dict)

            return serialize_object(message, dict), response

        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}
