import logging
from pprint import pprint

from zeep.helpers import serialize_object

from enedis.connection.enedis_connection import EnedisConnection

logger = logging.getLogger(__name__)


class M023Base:
    name = None
    ns = None
    tn_binding = None
    port_binding = None
    service_path = None
    soap_action = None

    @classmethod
    def m023(cls, connection: EnedisConnection, donnees, send=True):
        message, response = None, None
        try:
            service, factory, client = connection.soap_service(cls.name, cls.ns, cls.port_binding, cls.service_path,
                                                           cls.tn_binding)

            donnees['donneesGenerales']['contratId'] = connection.contract_id
            donnees['donneesGenerales']['initiateurLogin'] = connection.login

            if not cls.is_valid_request(donnees):
                raise ValueError('Vous avez fait le mauvais type de demande pour ce service')

            message = cls.create_factory_message(factory, **donnees)

            if send:
                soap_method = getattr(service, cls.soap_action)
                response_obj = soap_method(donneesGenerales=message['donneesGenerales'], demande=message['demande'])
                response = serialize_object(response_obj, dict)
            return serialize_object(message, dict), response
        except Exception as e:
            logger.exception("Erreur appel service")
            return message, {'erreur': str(e.args), 'status': 'failed'}

    @staticmethod
    def is_valid_request(donnees):
        # Logique de validation à implémenter pour chaque type de demande
        raise NotImplementedError

    @staticmethod
    def create_factory_message(_factory, **kwargs):
        # Logique de création du message pour chaque demande
        raise NotImplementedError

class M023HistoriqueMesuresFines(M023Base):
    name = 'B2B_M023MFI'
    ns = 'https://sge-b2b.enedis.fr/services/commandehistoriquedonneesmesuresfines/v1'
    tn_binding = 'https://sge-b2b.enedis.fr/services/commandehistoriquedonneesmesuresfines/v1'
    port_binding = 'AdamCommandeHistoriqueDonneesMesuresFinesBinding'
    service_path = 'CommandeHistoriqueDonneesMesuresFines/v1.0'
    soap_action = 'commandeHistoriqueDonneesMesuresFines'

    @classmethod
    def is_valid_request(cls, donnees):
        return "mesuresTypeCode" in donnees['demande']

    @classmethod
    def create_factory_message(cls, _factory, **kwargs):
        return _factory.demandePublicationMesuresFines(**kwargs)


class M023MesuresFacturantes(M023Base):
    name = 'B2B_M023MFA'
    ns = 'https://sge-b2b.enedis.fr/services/commandehistoriquedonneesmesuresfacturantes/v1'
    tn_binding = 'https://sge-b2b.enedis.fr/services/commandehistoriquedonneesmesuresfacturantes/v1'
    port_binding = 'AdamCommandeHistoriqueDonneesMesuresFacturantesBinding'
    service_path = 'CommandeHistoriqueDonneesMesuresFacturantes/v1.0'
    soap_action = 'commandeHistoriqueDonneesMesuresFacturantes'

    @classmethod
    def is_valid_request(cls, donnees):
        return "mesuresTypeCode" not in donnees['demande'] and 'dateDebut' in donnees['demande']

    @classmethod
    def create_factory_message(cls, _factory, **kwargs):
        return _factory.demandePublicationMesuresFacturantes(**kwargs)


class M023InformationsTechniquesEtContractuelles(M023Base):
    name = 'B2B_M023ITC'
    ns = 'https://sge-b2b.enedis.fr/services/commandeinformationstechniquesetcontractuelles/v1'
    tn_binding = 'https://sge-b2b.enedis.fr/services/commandeinformationstechniquesetcontractuelles/v1'
    port_binding = 'AdamCommandeInformationsTechniquesEtContractuellesBinding'
    service_path = 'CommandeInformationsTechniquesEtContractuelles/v1.0'
    soap_action = 'commandeInformationsTechniquesEtContractuelles'

    @classmethod
    def is_valid_request(cls, donnees):
        return "dateDebut" not in donnees['demande']

    @classmethod
    def create_factory_message(cls, _factory, **kwargs):
        return _factory.demandePublicationITC(**kwargs)

