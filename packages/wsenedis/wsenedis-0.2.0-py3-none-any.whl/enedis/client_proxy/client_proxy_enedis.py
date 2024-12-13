import datetime as dt
import enum
import json
import os
from json import JSONEncoder

import requests as r

from enedis.data_models.commandeaccesdonneesmesures import DemandeAccesDonneesMesures
from enedis.data_models.commanderarretservicesouscritmesures import DemandeArretServiceSouscritMesures
from enedis.data_models.commandercollectepublicationmesures import DemandeCollectePublicationMesure
from enedis.data_models.consulterdonneestechniquescontractuelles import ConsulterDonneesTechniquesContractuelles

from enedis.data_models.consultermesures import DonneesConsulterMesures
from enedis.data_models.consultermesuresdetaillees import \
    DemandeConsulterMesuresDetaillees
from enedis.data_models.recherchepoint import Criteres

__version__ = '1.0_dev'


def serializator(o):
    encoder = json.JSONEncoder()
    if isinstance(o, dt.time) or isinstance(o, dt.datetime) or isinstance(o, dt.date):
        return o.isoformat()
    if issubclass(o, enum.Enum):
        return o.value
    else:
        return encoder.default(o)


class ClientProxyEnedis:
    MACHINE = os.getenv('PROJECT_NAME', '')
    WEBSERVICES_ENEDIS_HOST = os.environ['WEBSERVICES_ENEDIS_HOST']
    WEBSERVICES_ENEDIS_ROOT_PATH = os.environ['WEBSERVICES_ENEDIS_ROOT_PATH']

    def _envoi(self, donnees, _adresse=None, serializer=None):
        donnees_complettes = {'serveur': self.MACHINE, 'donnees': {**donnees}}
        rep = r.post(_adresse, json=json.dumps(donnees_complettes, default=serializator or JSONEncoder)).json()
        return rep

    def commander_access_donnees_mesures(self, donnees: DemandeAccesDonneesMesures, version='v1.0'):
        adresse = f'{self.WEBSERVICES_ENEDIS_HOST}{self.WEBSERVICES_ENEDIS_ROOT_PATH}{version}/commandeaccesdonneesmesures'
        resultat = self._envoi(donnees, _adresse=adresse, serializer=serializator)
        return resultat

    def commander_arret_services_souscrits_mesures(self, donnees: DemandeArretServiceSouscritMesures, version='v1.0'):
        adresse = f'/{version}/commanderarretservicessouscritmesures'

        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat

    def commander_collecte_publication_mesures(self, donnees: DemandeCollectePublicationMesure,
                                               version='v3.0'):
        adresse = f'/{version}/commandercollectepublicationmesures'
        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat

    def consulter_donnees_techniques_contractuelles(self, donnees: ConsulterDonneesTechniquesContractuelles, version='v1.0'):
        adresse = f'/{version}/consulterdonneestechniquescontractuelles'
        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat

    def consulter_mesures(self, donnees: DonneesConsulterMesures, version='v1.0'):
        adresse = f'/{version}/consultermesures'
        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat

    def consulter_mesures_detaillees(self, donnees: DemandeConsulterMesuresDetaillees, version='v3.0'):
        adresse = f'/{version}/consultermesuresdetaillees'
        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat

    def rechercher_point(self, donnees: Criteres, version='v2.0'):
        adresse = f'/{version}/recherchepoint'
        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat

    def recherche_services_souscrits_mesures(self, point_id: str, version='v1.0'):
        adresse = f'/{version}/rechercheservicessouscritsmesures'
        donnees = {'pointId': point_id}
        resultat = self._envoi(donnees, _adresse=adresse)
        return resultat
