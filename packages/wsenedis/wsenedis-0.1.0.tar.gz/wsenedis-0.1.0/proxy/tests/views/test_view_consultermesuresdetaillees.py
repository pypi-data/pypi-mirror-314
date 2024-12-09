import datetime as dt

from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.const import TypeDonnees, GrandeurPhysique, SensMesure, CadreAcces
from enedis.data_models.consultermesuresdetaillees import \
    DemandeConsulterMesuresDetaillees


class TestViewConsulterMesuresDetaillees(TestCase):
    maxDiff = None

    def test_view_consultermesuresdetaillees(self):
        client = APIClient()

        test_data = {'serveur': 'poste_travail',
                     'donnees': DemandeConsulterMesuresDetaillees('12345678901234', TypeDonnees.CDC,
                                                                  GrandeurPhysique.TOUT,
                                                                  SensMesure.SOUTIRAGE,
                                                                  dt.date(2023, 1, 1), dt.date(2023, 12, 1), False,
                                                                  CadreAcces.ACCORD_CLIENT)
                     }

        reponse = client.post('/ws/v3.0/consultermesuresdetaillees/', test_data, format='json')

        resultat_attendu = {'pointId': 'string', 'mesuresCorrigees': 'BEST',
                            'periode': {
                                'dateDebut': '2013-10-10', 'dateFin': '2019-08-15'},
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
                                    'etapeMetier': 'string', 'contexteReleve': 'FMR', 'typeReleve': 'AP',
                                    'motifReleve': 'string',
                                    'grandeur': [
                                        {
                                            'grandeurMetier': 'PROD', 'grandeurPhysique': 'E', 'unite': 'string',
                                            'calendrier': [
                                                {
                                                    'idCalendrier': 'string', 'libelleCalendrier': 'string',
                                                    'classeTemporelle': [
                                                        {
                                                            'idClasseTemporelle': 'string',
                                                            'libelleClasseTemporelle': 'string',
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
        self.assertDictEqual(resultat_attendu, reponse.json())
