
from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.commanderarretservicesouscritmesures import DonneesGeneralesArretService, ArretServiceSouscrit, \
    DemandeArretServiceSouscritMesures


class TestViewCommanderArretServiceSouscrit(TestCase):
    maxDiff = None

    def test_view_commanderarretservicessouscrits(self):
        client = APIClient()
        arret_service_souscrit = ArretServiceSouscrit('12')
        donnees_generales = DonneesGeneralesArretService('12345678911234')
        demande_arret = DemandeArretServiceSouscritMesures(donnees_generales, arret_service_souscrit)
        entrees = {'serveur': 'poste_travail', 'donnees': demande_arret}
        reponse = client.post('/ws/v1.0/commanderarretservicessouscritmesures/', entrees, format='json')
        resultat_attendu = {'header': {
            'acquittement': None
        },
            'body': {
                'affaireId': 'string',
                'prestations': {
                    'prestation': [
                        {
                            'rang': 100,
                            'fiche': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'option': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'cas': {
                                'libelle': 'string', 'code': 'string'
                            }
                        }
                    ]
                }
            }
        }
        self.assertDictEqual(reponse.json(), resultat_attendu)