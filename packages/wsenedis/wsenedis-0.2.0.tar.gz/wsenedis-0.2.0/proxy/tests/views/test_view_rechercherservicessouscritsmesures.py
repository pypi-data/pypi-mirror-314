
from django.test import TestCase
from rest_framework.test import APIClient


class TestViewRechercheServicessouscritsMesures(TestCase):
    maxDiff = None

    def test_view_rechercherservicessouscritsmesures(self):
        client = APIClient()

        entree = {'serveur': 'poste_travail', 'donnees': {'criteres': {'pointId': '12345678911234'}}}
        reponse = client.post('/ws/v1.0/rechercheservicessouscritsmesures/', entree, format='json')
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
        self.assertDictEqual(reponse.json(), resultat_attendu)
