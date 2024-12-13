import datetime as dt
from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.const import *
from enedis.data_models.consultermesuresdetaillees import \
    DemandeConsulterMesuresDetaillees
from enedis.services.consulter_mesures_detaillees import ConsulterMesuresDetaillees
from proxy.tests.services.ServicesTestCase import raise_transport_errror, ServicesTestCase


class TestConsulterMesuresDetaillees(ServicesTestCase):
    maxDiff = None

    def test_creation_message(self):
        donnees = DemandeConsulterMesuresDetaillees('12345678911234', TypeDonnees.CDC, GrandeurPhysique.TOUT, SensMesure.SOUTIRAGE,
                                                    dt.date(2023, 1, 1), dt.date(2023, 12, 1), False, CadreAcces.ACCORD_CLIENT, MesuresPas.JOUR)

        msg, _ = ConsulterMesuresDetaillees.consulter_mesures_detaillees(self.connection, donnees, send=False)
        expected_message = {'demande':
            {'initiateurLogin': 'test@test.fr', 'pointId': '12345678911234', 'mesuresTypeCode': 'COURBE',
             'grandeurPhysique': 'TOUT', 'dateDebut': dt.date(2023, 1, 1), 'dateFin': dt.date(2023, 12, 1),
             'mesuresPas': 'P1D', 'mesuresCorrigees': False, 'sens': 'SOUTIRAGE', 'cadreAcces': 'ACCORD_CLIENT'}}

        self.assertDictEqual(msg, expected_message)

    def test_creation_message_errone(self):
        donnees = DemandeConsulterMesuresDetaillees('12345678911234', TypeDonnees.CDC, GrandeurPhysique.TOUT,
                                                    SensMesure.SOUTIRAGE,
                                                    dt.date.today(), dt.date.today(), None,
                                                    CadreAcces.ACCORD_CLIENT)


        _, response = ConsulterMesuresDetaillees.consulter_mesures_detaillees(self.connection, donnees)
        self.assertEqual(response['erreur'], "('Missing element mesuresCorrigees',)",
                         'attention le programme continue normalement alors qu\'il manque un élément dans les entrées')

    def test_connexion(self):
        donnees = DemandeConsulterMesuresDetaillees('12345678911234', TypeDonnees.CDC, GrandeurPhysique.TOUT,
                                                    SensMesure.SOUTIRAGE,
                                                    dt.date(2023, 1, 1), dt.date(2023, 12, 1), False,
                                                    CadreAcces.ACCORD_CLIENT)

        _, response = ConsulterMesuresDetaillees.consulter_mesures_detaillees(self.connection, donnees)

        expected_response = {'pointId': 'string', 'mesuresCorrigees': 'BEST',
                            'periode': {
                                'dateDebut': dt.date(2013, 10, 10), 'dateFin': dt.date(2019, 8, 15)},
                            'grandeur': [
                                {
                                    'grandeurMetier': 'PROD', 'grandeurPhysique': 'PA', 'unite': 'string',
                                    'points': [
                                        {
                                            'v': 'string', 'd': 'string', 'p': 'string', 'n': 'string', 'tc': 'string',
                                            'iv': 'string', 'ec': 'string'
                                        }
                                    ]
                                }
                            ],
                            'contexte': [
                                {
                                    'etapeMetier': 'string', 'contexteReleve': 'FMR', 'typeReleve': 'AP', 'motifReleve': 'string',
                                    'grandeur': [
                                        {
                                            'grandeurMetier': 'PROD', 'grandeurPhysique': 'E', 'unite': 'string',
                                            'calendrier': [
                                                {
                                                    'idCalendrier': 'string', 'libelleCalendrier': 'string',
                                                    'classeTemporelle': [
                                                        {
                                                            'idClasseTemporelle': 'string', 'libelleClasseTemporelle': 'string',
                                                            'codeCadran': 'string',
                                                            'valeur': [
                                                                {
                                                                    'd': 'string', 'v': 100, 'iv': 2
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ],
                                            'cadranTotalisateur': {
                                                'codeCadran': 'string',
                                                'valeur': [
                                                    {
                                                        'd': 'string', 'v': 100, 'iv': 2
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            ], 'typeValeur': 'string', 'modeCalcul': 'string', 'pas': 'string'
                            }

        self.assertDictEqual(response, expected_response)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        donnees = DemandeConsulterMesuresDetaillees('12345678911234', TypeDonnees.CDC, GrandeurPhysique.TOUT,
                                                    SensMesure.SOUTIRAGE,
                                                    dt.date(2023, 1, 1), dt.date(2023, 12, 1), False,
                                                    CadreAcces.ACCORD_CLIENT)

        _, response = ConsulterMesuresDetaillees.consulter_mesures_detaillees(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})




