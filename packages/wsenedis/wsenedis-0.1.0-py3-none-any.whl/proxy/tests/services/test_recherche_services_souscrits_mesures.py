import datetime as dt
from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.rechercheservicesouscritmesures import RechercherServicesSouscritsMesures, Criteres
from enedis.services.recherche_services_souscrits_mesures import RechercheServicesSouscritsMesures
from proxy.tests.services.ServicesTestCase import raise_transport_errror, raise_creation_error, ServicesTestCase


class TestRecherche(ServicesTestCase):
    maxDiff = None
    def test_creation_message(self):
        donnees = RechercherServicesSouscritsMesures(Criteres('12345678911234'))
        msg, _ = RechercheServicesSouscritsMesures.rechercher_services_souscrit_mesures(self.connection, donnees, send=False)
        self.assertDictEqual(msg, {'criteres': {'contratId': '1111111', 'pointId': '12345678911234'},
                                   'loginUtilisateur': 'test@test.fr'})

    def test_connexion(self):
        donnees = RechercherServicesSouscritsMesures(Criteres('12345678911234'))

        _, response = RechercheServicesSouscritsMesures.rechercher_services_souscrit_mesures(self.connection, donnees)

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
                            'serviceSouscritLibelle': 'string', 'injection': False, 'soutirage': False, 'contratId': 'string',
                            'contratLibelle': 'string', 'etatCode': 'string', 'dateDebut': dt.date(2005, 9, 2), 'dateFin': dt.date(2019, 8, 6),
                            'motifFinLibelle': 'string', 'mesuresTypeCode': 'string', 'mesuresPas': 'string',
                            'mesuresCorrigees': False, 'periodiciteTransmission': 'string'
                        }
                    ]
                }
            }
        }

        self.assertDictEqual(response, resultat_attendu)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        donnees = RechercherServicesSouscritsMesures(Criteres('12345678911234'))
        _, response = RechercheServicesSouscritsMesures.rechercher_services_souscrit_mesures(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})






