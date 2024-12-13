from pprint import pprint

from enedis.data_models.M023 import *
from enedis.data_models.const import *
from enedis.services.commande_M023 import M023InformationsTechniquesEtContractuelles, M023MesuresFacturantes, M023HistoriqueMesuresFines
from proxy.tests.services.ServicesTestCase import ServicesTestCase


class TestM023(ServicesTestCase):
    maxDiff = None

    def test_connexion(self):
        donnees = DemandeInformationsTechniquesEtContractuelles(CadreAcces.ACCORD_CLIENT,
                                                                SensMesure.SOUTIRAGE, ['12345678911234'],
                                                                FormatsM023.JSON)
        msg, response = M023InformationsTechniquesEtContractuelles.m023(self.connection, donnees)
        pprint(msg)
        self.assertDictEqual(msg, {'demande': {'cadreAcces': 'ACCORD_CLIENT',
                                               'format': 'JSON',
                                               'pointIds': [{'pointId': '12345678911234'}],
                                               'sens': 'SOUTIRAGE'},
                                   'donneesGenerales': {'affaireReference': None,
                                                        'contratId': '1111111',
                                                        'initiateurLogin': 'test@test.fr',
                                                        'referenceDemandeur': None,
                                                        'referenceRegroupement': None}}
                             )
        self.assertEqual(response, 'string')

        donnees = DemandeHistoriqueDonneesFacturantes(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT,
                                                      SensMesure.SOUTIRAGE,
                                                      ['12345678911234'],
                                                      FormatsM023.CSV)
        msg, response = M023MesuresFacturantes.m023(self.connection, donnees)
        self.assertDictEqual(msg, {'demande': {'cadreAcces': 'ACCORD_CLIENT',
                                               'dateDebut': dt.date(2023, 1, 1),
                                               'dateFin': dt.date(2023, 6, 1),
                                               'format': 'CSV',
                                               'pointIds': [{'pointId': '12345678911234'}],
                                               'sens': 'SOUTIRAGE'},
                                   'donneesGenerales': {'affaireReference': None,
                                                        'contratId': '1111111',
                                                        'initiateurLogin': 'test@test.fr',
                                                        'referenceDemandeur': None,
                                                        'referenceRegroupement': None}})
        self.assertEqual(response, 'string')

        donnees = DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                dt.date(2023, 6, 1),
                                                CadreAcces.ACCORD_CLIENT,
                                                SensMesure.SOUTIRAGE,
                                                TypeDonneesM023.CDC,
                                                ['12345678911234'],
                                                FormatsM023.JSON,
                                                True)

        msg, response = M023HistoriqueMesuresFines.m023(self.connection, donnees)
        self.assertDictEqual(msg, {'demande': {'cadreAcces': 'ACCORD_CLIENT',
                                               'dateDebut': dt.date(2023, 1, 1),
                                               'dateFin': dt.date(2023, 6, 1),
                                               'format': 'JSON',
                                               'mesuresCorrigees': True,
                                               'mesuresTypeCode': 'COURBES',
                                               'pointIds': [{'pointId': '12345678911234'}],
                                               'sens': 'SOUTIRAGE'},
                                   'donneesGenerales': {'affaireReference': None,
                                                        'contratId': '1111111',
                                                        'initiateurLogin': 'test@test.fr',
                                                        'referenceDemandeur': None,
                                                        'referenceRegroupement': None}})
        self.assertEqual(response, 'string')

    def test_mauvaises_dates(self):

        self.assertRaises(ValueError, DemandeHistoriqueDonneesFacturantes, dt.date(2023, 2, 1),
                                                      dt.date(2023, 1, 1),
                                                      CadreAcces.ACCORD_CLIENT,
                                                      SensMesure.SOUTIRAGE,
                                                      ['12345678911234'],
                                                      FormatsM023.CSV)