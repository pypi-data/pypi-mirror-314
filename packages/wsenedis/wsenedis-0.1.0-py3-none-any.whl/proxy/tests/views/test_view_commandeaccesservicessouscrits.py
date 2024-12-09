
from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.commandeaccesdonneesmesures import *
from enedis.data_models.common import *


class TestViewCommandeAccesServicesSouscrit(TestCase):
    maxDiff = None

    def test_view_commanderaccesservicessouscrits(self):
        client = APIClient()
        personne_morale = PersonneMorale('denominationsociale')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_donnees = AccesDonnees(dt.date(2020, 6, 22), dt.date(2022, 6, 22), TypeDonneesV1.CDC,
                                     TypeSite.SOUTIRAGE,
                                     declaration_accord_client)
        donnees_generales = DonneesGeneralesAccesDonnees('12345678911234', Contrat())
        donnees = DemandeAccesDonneesMesures(donnees_generales, acces_donnees)
        entrees = {'serveur': 'poste_travail', 'donnees': donnees}
        reponse = client.post('/ws/v1.0/commandeaccesdonneesmesures/', entrees, format='json')

        resultat_attendu = {'header':
            {
                'acquittement': None},
            'body': {
                'affaireId': 'string',
                'prestations': {
                    'prestation': {
                        'rang': 100,
                        'fiche': {
                            'libelle': 'string', 'code': 'string'
                        },
                        'option': {
                            'libelle': 'string', 'code': 'string'
                        }, 'cas': {
                            'libelle': 'string', 'code': 'string'
                        }
                    }
                }, 'serviceSouscritId': 'string'
            }
        }
        self.assertDictEqual(reponse.json(), resultat_attendu)