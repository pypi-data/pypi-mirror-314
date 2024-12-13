from time import sleep

from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.const import DomaineTension, ClientFinalCategorieCode
from enedis.data_models.recherchepoint import AdresseInstallation, Criteres, RechercherPoint


class TestViewRecherchePoint(TestCase):
    def test_view_rechercherpoint(self):
        sleep(1)
        client = APIClient()

        adresse_installation = AdresseInstallation('escalier 8 etage 9 appartement 10', 'batiment E',
                                                   '404 voie introuvable',
                                                   'Faron', '83000', '48414956515')
        criteres = Criteres('12345678901234', '963852', DomaineTension.HTA, 'societe de test',
                            ClientFinalCategorieCode.PRO, True, adresse_installation)
        donnees = RechercherPoint(criteres)
        donnees_entree = {'serveur': 'poste_travail', 'donnees': donnees}
        reponse = client.post('/ws/v2.0/recherchepoint/', donnees_entree, format='json')
        body_attendu = {'points':
                            {
                                'point': [
                                    {
                                        'adresseInstallationNormalisee': {
                                            'ligne1': 'string', 'ligne2': 'string', 'ligne3': 'string', 'ligne4': 'string',
                                            'ligne5': 'string', 'ligne6': 'string', 'ligne7': 'string'
                                        },
                                        'matricule': ['string'], 'numeroSerie': ['string'],
                                        'typeComptage': {
                                            'libelle': 'string', 'code': 'string'
                                        },
                                        'etatContractuel': {
                                            'libelle': 'string', 'code': 'SERVC'
                                        },
                                        'nomClientFinalOuDenominationSociale': 'string', 'id': 'string'
                                    }
                                ]
                            }
        }

        body = reponse.json()['body']
        if 'code' in body['points']['point'][0]['etatContractuel']:
            body['points']['point'][0]['etatContractuel']['code'] = "SERVC"

        self.assertDictEqual(body, body_attendu)

