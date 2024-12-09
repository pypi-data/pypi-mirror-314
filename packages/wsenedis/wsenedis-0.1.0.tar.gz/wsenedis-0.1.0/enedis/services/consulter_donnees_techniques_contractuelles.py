import logging

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.consulterdonneestechniquescontractuelles import ConsulterDonneesTechniquesContractuelles

logger = logging.getLogger(__name__)

class ConsulterDoneesTechniquesContractuelles:
    name = 'ConsultationDonneesTechniquesContractuelles-v1.0'
    ns = 'http://www.enedis.fr/sge/b2b/services/consulterdonneestechniquescontractuelles/v1.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/services/consultationdonneestechniquescontractuelles/v1.0'
    port_binding = 'ConsultationDonneesTechniquesContractuellesBinding'
    service_path = 'ConsultationDonneesTechniquesContractuelles/v1.0'

    @classmethod
    def consultation_donnees_techniques_contractuelles(cls, connection:EnedisConnection, donnees: ConsulterDonneesTechniquesContractuelles, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            donnees['loginUtilisateur'] = connection.login

            # Contrairement aux autres types, passer l'objet donnees directement ne fonctionne pas
            message = factory.ConsulterDonneesTechniquesContractuellesType(**donnees)

            if send:
                # Contrairement aux autres services, passer l'objet message directement ne fonctionne pas
                response = serialize_object(service.consulterDonneesTechniquesContractuelles(**{k:message[k] for k,v in donnees.items()}), dict)

            return serialize_object(message, dict), response
        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}