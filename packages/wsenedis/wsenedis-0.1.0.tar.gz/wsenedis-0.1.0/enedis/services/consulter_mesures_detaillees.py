import logging

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.consultermesuresdetaillees import \
    DemandeConsulterMesuresDetaillees
from utils.regex import verification_prm

logger = logging.getLogger(__name__)

class ConsulterMesuresDetaillees:
    name = 'ADAM.ConsulterMesuresServiceReadV3'
    ns = 'http://www.enedis.fr/sge/b2b/services/consultationmesuresdetaillees/common'
    tn_binding = 'http://www.enedis.fr/sge/b2b/services/consultationmesuresdetaillees/v3.0'
    port_binding = 'AdamConsultationMesuresServiceReadHttpBinding'
    service_path = 'ConsultationMesuresDetaillees/v3.0'

    @classmethod
    def consulter_mesures_detaillees(cls, connection: EnedisConnection, donnees: DemandeConsulterMesuresDetaillees, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            donnees['initiateurLogin'] = connection.login
            message = factory.ConsulterMesuresDetailleesV3Type(donnees)
            if send:
                response = serialize_object(service.consulterMesuresDetailleesV3(message), dict)

            return serialize_object(message, dict), response
        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}
