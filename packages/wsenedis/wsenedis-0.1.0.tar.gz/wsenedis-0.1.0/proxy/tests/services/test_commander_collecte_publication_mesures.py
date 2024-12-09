from pprint import pprint
from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.commandercollectepublicationmesures import *
from enedis.data_models.common import PersonneMorale
from enedis.services.commander_collecte_publication_mesures import CommanderCollectePublicationMesures
from proxy.tests.services.ServicesTestCase import ServicesTestCase, raise_transport_errror, raise_creation_error


class TestCommaderCollectePublicationMesures(ServicesTestCase):


    def test_creation_message_correct(self):
        personne_morale = PersonneMorale('personnemoraleclient')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_mesures = AccesMesures(dt.date.today(), dt.date.today(), declaration_accord_client, TypeDonneesV1.INDEX, False,
                                     True, PasMesures.QUOTIDIEN, True,
                                     PeriodiciteTransmission.QUOTIDIENNE, False)
        donnees_generales = DonneesGeneralesDemandeCollecte('12345678911234')
        donnees = DemandeCollectePublicationMesure(donnees_generales, acces_mesures)

        msg, _ = CommanderCollectePublicationMesures.commander_collecte_publication(self.connection, donnees, send=False)
        expected_msg = {'demande': {
            'donneesGenerales': {
                'initiateurLogin': 'test@test.fr', 'contratId': '1111111', 'objetCode': 'AME', 'pointId': '12345678911234'
            },
            'accesMesures': {
                'dateDebut': dt.date.today(), 'dateFin': dt.date.today(), 'mesuresTypeCode': 'IDX',
                'mesuresPas': 'P1D', 'mesuresCorrigees': False, 'transmissionRecurrente': True,
                'periodiciteTransmission': 'P1D', 'injection': True, 'soutirage': False, 'declarationAccordClient': {
                    'accord': True,
                    'personneMorale': {
                        'denominationSociale': 'personnemoraleclient'}}}}}

        self.assertDictEqual(msg, expected_msg)

    def test_creation_message_malforme(self):
        personne_morale = PersonneMorale('personnemoraleclient')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_mesures = AccesMesures(None, dt.date.today(), declaration_accord_client, TypeDonneesV1.INDEX, False,
                                     True, PasMesures.QUOTIDIEN, True,
                                     PeriodiciteTransmission.QUOTIDIENNE, False)
        donnees_generales = DonneesGeneralesDemandeCollecte('12345678911234')
        donnees = DemandeCollectePublicationMesure(donnees_generales, acces_mesures)

        msg, response = CommanderCollectePublicationMesures.commander_collecte_publication(self.connection, donnees, send=True)
        self.assertEqual(response['erreur'], "('Missing element dateDebut',)", "le programme ne renvoie pas d'erreur alors qu'il manque un élément")

    def test_connexion(self):
        personne_morale = PersonneMorale('personnemoraleclient')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_mesures = AccesMesures(dt.date.today(), dt.date.today(), declaration_accord_client, TypeDonneesV1.INDEX,
                                     False,
                                     True, PasMesures.QUOTIDIEN, True,
                                     PeriodiciteTransmission.QUOTIDIENNE, False)
        donnees_generales = DonneesGeneralesDemandeCollecte('12345678911234')
        donnees = DemandeCollectePublicationMesure(donnees_generales, acces_mesures)
        _, response = CommanderCollectePublicationMesures.commander_collecte_publication(self.connection, donnees)

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
                            }
                        }
                    ]
                }
                , 'serviceSouscritId': 'string'
            }
        }

        self.assertDictEqual(response, expected_response)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        personne_morale = PersonneMorale('personnemoraleclient')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_mesures = AccesMesures(dt.date.today(), dt.date.today(), declaration_accord_client, TypeDonneesV1.INDEX, False,
                                     True, PasMesures.QUOTIDIEN, True,
                                     PeriodiciteTransmission.QUOTIDIENNE, False)
        donnees_generales = DonneesGeneralesDemandeCollecte('12345678911234')
        donnees = DemandeCollectePublicationMesure(donnees_generales, acces_mesures)
        msg, response = CommanderCollectePublicationMesures.commander_collecte_publication(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})


