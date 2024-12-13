import datetime as dt
from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.commandercollectepublicationmesures import AccesMesures, DonneesGeneralesDemandeCollecte, \
    DemandeCollectePublicationMesure
from enedis.data_models.common import PersonneMorale, DeclarationAccordClient
from enedis.data_models.const import *


class TestViewCommanderCollectePublicationMesures(TestCase):
    maxDiff = None

    def test_view_commandercollectepublicationmesures(self):
        client = APIClient()
        personne_morale = PersonneMorale('personnemoraleclient')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_mesures = AccesMesures(dt.date.today(), dt.date.today(), declaration_accord_client, TypeDonneesV1.INDEX,
                                     False,
                                     True, PasMesures.QUOTIDIEN, True,
                                     PeriodiciteTransmission.QUOTIDIENNE, False)
        donnees_generales = DonneesGeneralesDemandeCollecte('12345678911234')
        donnees = DemandeCollectePublicationMesure(donnees_generales, acces_mesures)
        entrees = {'serveur': 'poste_travail', 'donnees': donnees}
        reponse = client.post('/ws/v3.0/commandercollectepublicationmesures/', entrees, format='json')
        resultat_attendu = {'header': {
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
                            }
                        }
                    ]
                }
                , 'serviceSouscritId': 'string'
            }
        }
        self.assertEqual(reponse.json(), resultat_attendu, "echec du test de connexion  avec imposter")
