from unittest.mock import patch

import zeep
from zeep.helpers import serialize_object

from enedis.data_models.commandeaccesdonneesmesures import *
from enedis.data_models.common import *
from enedis.data_models.const import TypeDonneesV1
from enedis.services.commande_acces_donnees_mesures import CommandeAccesDonneesMesures
from proxy.tests.services.ServicesTestCase import ServicesTestCase, raise_transport_errror


class TestCommandeAccesDonneesMesures(ServicesTestCase):
    maxDiff = None

    def test_acreation_message_correct(self):
        personne_morale = PersonneMorale('denominationsociale')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_donnees = AccesDonnees(dt.date(2020, 6, 22),
                                     dt.date(2022, 6, 22),
                                     TypeDonneesV1.CDC,
                                     TypeSite.SOUTIRAGE,
                                     declaration_accord_client)
        contrat = Contrat()
        donnees_generales = DonneesGeneralesAccesDonnees('12345678911234', contrat)
        donnees = DemandeAccesDonneesMesures(donnees_generales, acces_donnees)

        message, _ = CommandeAccesDonneesMesures.commande_acces_donnees_mesures(self.connection, donnees, send=False)
        expected_message = {
            'demande':{
                'donneesGenerales': {
                    'objetCode': 'AME',
                    'pointId': '12345678911234',
                    'initiateurLogin': 'test@test.fr',
                    'contrat': {
                        'contratId': '1111111'
                    }
                },
                'accesDonnees': {
                    'dateDebut': dt.date(2020, 6, 22),
                    'dateFin': dt.date(2022, 6, 22),
                    'typeDonnees': 'CDC',
                    'declarationAccordClient': {
                        'accord': True,
                        'personneMorale': {
                            'denominationSociale': 'denominationsociale'
                        },
                    },
                    'soutirage': True
                }
            }
        }
        self.assertDictEqual(message, expected_message)


    def test_avec_id_malforme(self):
        personne_morale = PersonneMorale('denominationsociale')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_donnees = AccesDonnees(dt.date(2020, 6, 22), dt.date(2022, 6, 22), TypeDonneesV1.CDC,
                                     TypeSite.SOUTIRAGE,
                                     declaration_accord_client)
        contrat = Contrat()

        donnees_generales = DonneesGeneralesAccesDonnees('1234', contrat)
        donnees = DemandeAccesDonneesMesures(donnees_generales, acces_donnees)

        msg, response = CommandeAccesDonneesMesures.commande_acces_donnees_mesures(self.connection, donnees)
        self.assertEqual(response['erreur'], "('le champ point_id doit être une chaine de 14 caractères numériques',)"
                         , "la vérification de la validité de l'id ne fonctionne plus")


    def test_transmission_message(self):
        personne_morale = PersonneMorale('denominationsociale')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_donnees = AccesDonnees(dt.date(2020, 6, 22), dt.date(2022, 6, 22), TypeDonneesV1.CDC,
                                     TypeSite.SOUTIRAGE,
                                     declaration_accord_client)
        contrat = Contrat()
        donnees_generales = DonneesGeneralesAccesDonnees('12345678911234', contrat)
        donnees = DemandeAccesDonneesMesures(donnees_generales, acces_donnees)
        _, response = CommandeAccesDonneesMesures.commande_acces_donnees_mesures(self.connection, donnees)

        expected_response = {
            'header':
                {
                    'acquittement': None
                },
            'body':
                {
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

        self.assertDictEqual(response, expected_response, "echec du test de connexion  avec imposter")

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        """
        ./manage.py test tests.test_commandeaccesservicessouscrits.TestCommandeAccesServicesSousCrits.test_connexion_echoue
        """
        personne_morale = PersonneMorale('denominationsociale')
        declaration_accord_client = DeclarationAccordClient(personne_morale, accord=True)
        acces_donnees = AccesDonnees(dt.date(2020, 6, 22), dt.date(2022, 6, 22), TypeDonneesV1.CDC,
                                     TypeSite.SOUTIRAGE,
                                     declaration_accord_client)
        contrat = Contrat()
        donnees_generales = DonneesGeneralesAccesDonnees('12345678911234', contrat)
        donnees = DemandeAccesDonneesMesures(donnees_generales, acces_donnees)
        msg, response = CommandeAccesDonneesMesures.commande_acces_donnees_mesures(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})

