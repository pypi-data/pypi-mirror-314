import logging
from pprint import pprint

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.consulterdonneespoint import DonneesConsulterPoint

logger = logging.getLogger(__name__)


class ConsulterPoint:
    ns = 'http://www.enedis.fr/sge/b2b/services/consulterdonneespoint/v4.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/services/consultationpoint/v4.0'
    name = 'ConsultationPoint-v4.0'
    service_name = 'consulterDonneesPoint'
    service_path = 'ConsultationPoint/v4.0'
    port_binding = 'ConsultationPointBinding'

    @classmethod
    def consulter_donnees_point(cls, connection: EnedisConnection, donnees: DonneesConsulterPoint, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                       cls.tn_binding)

            donnees['loginUtilisateur'] = connection.login

            message = factory.ConsulterDonneesPointType(**donnees)

            if send:
                response = serialize_object(service.consulterDonneesPoint(**{k:message[k] for k,v in donnees.items()}), dict)

            return serialize_object(message, dict), response

        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}

