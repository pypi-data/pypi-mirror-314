from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.consultermesures import DonneesConsulterMesures


class TestViewConsulterMesures(TestCase):
    maxDiff = None

    def test_view_consultermesures(self):
        client = APIClient()
        datas = {'serveur': 'poste_travail', 'donnees': DonneesConsulterMesures('12345678911234', True)}
        reponse = client.post('/ws/v1.1/consultermesures/', datas, format='json')
        resultat_attendu = {
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
                                        'valeur': 100, 'dateDebut': '2019-09-25',
                                        'dateFin': '2004-11-30',
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
                                        'valeur': 100, 'dateDebut': '2011-05-04',
                                        'dateFin': '2012-03-25',
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
        self.assertDictEqual(reponse.json(), resultat_attendu)



