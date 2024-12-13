import logging

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.consultermesures import DonneesConsulterMesures
from enedis.utils.regex import verification_prm

logger = logging.getLogger(__name__)

class ConsulterMesures:
    name = 'ConsultationMesures-v1.1'
    ns = 'http://www.enedis.fr/sge/b2b/services/consultermesures/v1.1'
    tn_binding = 'http://www.enedis.fr/sge/b2b/services/consultationmesures/v1.1'
    port_binding = 'ConsultationMesuresBinding'
    service_path = 'ConsultationMesures/v1.1'

    @classmethod
    def consulter_mesures(cls, connection:EnedisConnection, donnees: DonneesConsulterMesures, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            verification_prm(donnees['pointId'])

            donnees['loginDemandeur'] = connection.login
            donnees['contratId'] = connection.contract_id

            message = factory.ConsulterMesuresType(**donnees)

            if send:
                response = serialize_object(service.consulterMesures(**{k:message[k] for k,v in donnees.items()}), dict)
            return serialize_object(message), response
        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}

