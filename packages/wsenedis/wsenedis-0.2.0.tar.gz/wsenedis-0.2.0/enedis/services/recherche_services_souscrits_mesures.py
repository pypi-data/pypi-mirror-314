import logging

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection
from enedis.data_models.rechercheservicesouscritmesures import RechercherServicesSouscritsMesures

logger = logging.getLogger(__name__)

class RechercheServicesSouscritsMesures:
    name = 'RechercheServicesSouscritsMesures'
    ns = 'http://www.enedis.fr/sge/b2b/rechercherservicessouscritsmesures/v1.0'
    tn_binding = 'http://www.enedis.fr/sge/b2b/rechercheservicessouscritsmesures/v1.0'
    port_binding = 'RechercheServicesSouscritsMesuresBinding'
    service_path = 'RechercheServicesSouscritsMesures/v1.0'

    @classmethod
    def rechercher_services_souscrit_mesures(cls, connection: EnedisConnection, donnees: RechercherServicesSouscritsMesures, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            donnees['loginUtilisateur'] = connection.login
            donnees['criteres']['contratId'] = connection.contract_id
            message = factory.RechercherServicesSouscritsMesuresType(criteres=donnees['criteres'], loginUtilisateur=connection.login)

            if send:
                response = serialize_object(service.rechercherServicesSouscritsMesures(**{k:message[k] for k,v in donnees.items()}), dict)

            return serialize_object(message, dict), response

        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}
