from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.commanderarretservicesouscritmesures import *
from enedis.services.commander_arret_service_souscrit_mesures import CommanderArretServiceSouscritMesures
from proxy.tests.services.ServicesTestCase import ServicesTestCase, raise_transport_errror, raise_creation_error


class TestCommanderArretServicesSouscritsMesures(ServicesTestCase):
    maxDiff = None

    def test_creation_message(self):
        arret_service_souscrit = ArretServiceSouscrit('12')
        donnees_generales = DonneesGeneralesArretService('12345678911234')
        demande_arret = DemandeArretServiceSouscritMesures(donnees_generales, arret_service_souscrit)

        msg, _ = CommanderArretServiceSouscritMesures.commander_arret_service_souscrit_mesures(self.connection, demande_arret, send=False)

        expected_msg = {'demande': {
            'donneesGenerales': {
                'objetCode': 'ASS',
                'pointId': '12345678911234',
                'initiateurLogin': 'test@test.fr',
                'contratId': '1111111'
            },
            'arretServiceSouscrit': {
                'serviceSouscritId': '12'}}}

        self.assertDictEqual(msg, expected_msg)

    def test_transmission_message(self):
        arret_service_souscrit = ArretServiceSouscrit('12')
        donnees_generales = DonneesGeneralesArretService('12345678911234')
        demande_arret = DemandeArretServiceSouscritMesures(donnees_generales, arret_service_souscrit)

        msg, response = CommanderArretServiceSouscritMesures.commander_arret_service_souscrit_mesures(self.connection, demande_arret)

        expected_response = {'header': {
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
        self.assertDictEqual(response, expected_response)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        arret_service_souscrit = ArretServiceSouscrit('12')
        donnees_generales = DonneesGeneralesArretService('12345678911234')
        demande_arret = DemandeArretServiceSouscritMesures(donnees_generales, arret_service_souscrit)
        msg, response = CommanderArretServiceSouscritMesures.commander_arret_service_souscrit_mesures(self.connection, demande_arret)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})

