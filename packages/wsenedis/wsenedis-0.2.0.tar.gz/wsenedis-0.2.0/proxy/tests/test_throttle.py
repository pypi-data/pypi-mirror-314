from time import sleep

from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.recherchepoint import *
from enedis.data_models.rechercheservicesouscritmesures import RechercherServicesSouscritsMesures


class TestThrottle(TestCase):

    def setUp(self) -> None:
        sleep(1)

    def test_multiple_call_one_endpoint(self):
        client = APIClient()

        adresse_installation = AdresseInstallation('escalier 8 etage 9 appartement 10', 'batiment E',
                                                   '404 voie introuvable',
                                                   'Faron', '83000', '48414956515')
        criteres = Criteres('12345678901234', '963852', DomaineTension.HTA, 'societe de test',
                            ClientFinalCategorieCode.PRO, True, adresse_installation)
        donnees_recherche_point = RechercherPoint(criteres)
        donnees_entree = {'serveur': 'poste_travail', 'donnees': donnees_recherche_point}

        client.post('/ws/v2.0/recherchepoint/', donnees_entree, format='json')
        reponse = client.post('/ws/v2.0/recherchepoint/', donnees_entree, format='json')

        self.assertEqual(reponse.json()['detail'], 'Request was throttled. Expected available in 1 second.')


    def test_multiple_call_multiple_endpoints(self):
        client = APIClient()
        adresse_installation = AdresseInstallation('escalier 8 etage 9 appartement 10', 'batiment E',
                                                   '404 voie introuvable',
                                                   'Faron', '83000', '48414956515')
        criteres = Criteres('12345678901234', '963852', DomaineTension.HTA, 'societe de test',
                            ClientFinalCategorieCode.PRO, True, adresse_installation)
        donnees_recherche_point = RechercherPoint(criteres)

        donnees_recherche_service = {'serveur': 'poste_travail', 'donnees': RechercherServicesSouscritsMesures({'pointId': '12345678911234', 'contratId':''})}

        client.post('/ws/v2.0/recherchepoint/', {'serveur': 'poste_travail', 'donnees': donnees_recherche_point}, format='json')

        reponse = client.post('/ws/v1.0/rechercheservicessouscritsmesures/', donnees_recherche_service, format='json')

        resultat_attendu = {
            'header': {
                'acquittement': None
            },
            'body': {
                'servicesSouscritsMesures': {
                    'serviceSouscritMesures': [
                        {
                            'serviceSouscritId': 'string', 'pointId': 'string',
                            'serviceSouscritType': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'serviceSouscritLibelle': 'string', 'injection': False, 'soutirage': False,
                            'contratId': 'string',
                            'contratLibelle': 'string', 'etatCode': 'string', 'dateDebut': '2005-09-02',
                            'dateFin': '2019-08-06',
                            'motifFinLibelle': 'string', 'mesuresTypeCode': 'string', 'mesuresPas': 'string',
                            'mesuresCorrigees': False, 'periodiciteTransmission': 'string'
                        }
                    ]
                }
            }
        }
        self.assertEqual(reponse.json(), resultat_attendu)