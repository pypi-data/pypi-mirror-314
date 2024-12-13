import datetime as dt
from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.consultermesures import DonneesConsulterMesures
from enedis.services.consulter_mesures import ConsulterMesures
from proxy.tests.services.ServicesTestCase import raise_transport_errror, ServicesTestCase


class TestConsulterMesures(ServicesTestCase):
    maxDiff = None

    def test_creation_message_correct(self):
        donnees = DonneesConsulterMesures('12345678911234', autorisation_client=True)
        msg, _ = ConsulterMesures.consulter_mesures(self.connection, donnees, send=False)
        expected_msg = {'pointId': '12345678911234', 'loginDemandeur': 'test@test.fr', 'contratId': '1111111',
                            'contratConcluNouveauClientSurSite': None, 'autorisationClient': True}
        self.assertDictEqual(msg, expected_msg)

    def test_connexion(self):
        donnees = DonneesConsulterMesures('12345678911234', True)
        _, response = ConsulterMesures.consulter_mesures(self.connection, donnees)
        expected_response = {
            'header': {
                'acquittement': None
            },
            'body': {
                'seriesMesuresDateesGrilleTurpe': {
                    'serie': [
                        {
                            'grandeurPhysique': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'classeTemporelle': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'calendrier': {
                                'libelle': 'string', 'code': 'string'
                            }, 'unite': 'string',
                            'mesuresDatees': {
                                'mesure': [
                                    {
                                        'valeur': 100, 'dateDebut': dt.date(2019, 9, 25), 'dateFin': dt.date(2004, 11, 30),
                                        'nature': {
                                            'libelle': 'string', 'code': 'string'
                                        },
                                        'declencheur': {
                                            'libelle': 'string', 'code': 'string'
                                        },
                                        'statut': {
                                            'libelle': 'string', 'code': 'string'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                },
                'seriesMesuresDateesGrilleFrn': {
                    'serie': [
                        {
                            'grandeurPhysique': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'classeTemporelle': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'calendrier': {
                                'libelle': 'string', 'code': 'string'
                            },
                            'unite': 'string',
                            'mesuresDatees': {
                                'mesure': [
                                    {
                                        'valeur': 100, 'dateDebut': dt.date(2011, 5, 4), 'dateFin': dt.date(2012, 3, 25),
                                        'nature': {
                                            'libelle': 'string', 'code': 'string'
                                        },
                                        'declencheur': {
                                            'libelle': 'string', 'code': 'string'
                                        },
                                        'statut': {
                                            'libelle': 'string', 'code': 'string'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        self.assertDictEqual(response, expected_response)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        donnees = DonneesConsulterMesures('12345678911234', True)
        _, response = ConsulterMesures.consulter_mesures(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})

