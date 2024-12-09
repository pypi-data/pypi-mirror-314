from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.recherchepoint import *
from enedis.services.rechercher_point import RecherchePoint
from proxy.tests.services.ServicesTestCase import raise_transport_errror, ServicesTestCase


class TestRecherchePoint(ServicesTestCase):
    maxDiff = None

    def test_creation_message(self):
        adresse_installation = AdresseInstallation('escalier 8 etage 9 appartement 10', 'batiment E', '404 voie introuvable',
                                                   'Faron', '83000', '48414956515')
        criteres = Criteres('12345678901234', '963852', DomaineTension.HTA, 'societe de test', ClientFinalCategorieCode.PRO, True, adresse_installation)
        donnees = RechercherPoint(criteres)
        msg, _ = RecherchePoint.recherche_point(self.connection, donnees, send=False)
        expected_msg = {'criteres': {
            'adresseInstallation': {
                'escalierEtEtageEtAppartement': 'escalier 8 etage 9 appartement 10', 'batiment': 'batiment E',
                'numeroEtNomVoie': '404 voie introuvable', 'lieuDit': 'Faron', 'codePostal': '83000',
                'codeInseeCommune': '48414956515'
            },
            'numSiret': '12345678901234', 'matriculeOuNumeroSerie': '963852', 'domaineTensionAlimentationCode': 'HTA',
            'nomClientFinalOuDenominationSociale': 'societe de test', 'categorieClientFinalCode': 'PRO',
            'rechercheHorsPerimetre': True
        },
            'loginUtilisateur': 'test@test.fr'}

        self.assertDictEqual(msg, expected_msg)

    def test_connexion(self):
        adresse_installation = AdresseInstallation('escalier 8 etage 9 appartement 10', 'batiment E',
                                                   '404 voie introuvable',
                                                   'Faron', '83000', '48414956515')
        criteres = Criteres('12345678901234', '963852', DomaineTension.HTA, 'societe de test',
                            ClientFinalCategorieCode.PRO, True, adresse_installation)
        donnees = RechercherPoint(criteres)

        _, response = RecherchePoint.recherche_point(self.connection, donnees)

        if 'code' in response['body']['points']['point'][0]['etatContractuel']:
            response['body']['points']['point'][0]['etatContractuel']['code'] = 'SERVC'

        expected_response = {
            'header': {
                'acquittement': None
            },
            'body': {
                'points': {
                    'point': [
                        {
                            'adresseInstallationNormalisee': {
                                'ligne1': 'string', 'ligne2': 'string', 'ligne3': 'string', 'ligne4': 'string',
                                'ligne5': 'string', 'ligne6': 'string', 'ligne7': 'string'}, 'matricule': ['string'],
                            'numeroSerie': ['string'],
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
        }
        self.assertDictEqual(response, expected_response)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        adresse_installation = AdresseInstallation('escalier 8 etage 9 appartement 10', 'batiment E',
                                                   '404 voie introuvable',
                                                   'Faron', '83000', '48414956515')
        criteres = Criteres('12345678901234', '963852', DomaineTension.HTA, 'societe de test',
                            ClientFinalCategorieCode.PRO, True, adresse_installation)
        donnees = RechercherPoint(criteres)

        _, response = RecherchePoint.recherche_point(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})



