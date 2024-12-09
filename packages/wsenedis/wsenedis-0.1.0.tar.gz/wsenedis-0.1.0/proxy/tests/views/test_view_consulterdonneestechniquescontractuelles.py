from pprint import pprint

from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.M023 import DemandeInformationsTechniquesEtContractuelles, DemandeM023
from enedis.data_models.const import FormatsM023, SensMesure, CadreAcces
from enedis.data_models.consulterdonneestechniquescontractuelles import ConsulterDonneesTechniquesContractuelles


class TestViewConsulterDonneesTechniquesContractuelles(TestCase):
    maxDiff = None

    def test_view_consulterdonneestechniquescontractuelles(self):
        client = APIClient()
        datas = {'serveur': 'poste_travail', 'donnees': ConsulterDonneesTechniquesContractuelles('12345678901234', autorisation_client=True)}
        reponse = client.post('/ws/v1.0/consulterdonneestechniquescontractuelles/', datas, format='json')
        expected_result = dict(header={'acquittement': None},
                               body={
                                   'point': {
                                       'donneesGenerales': {'etatContractuel': {'libelle': 'string', 'code': 'RESIL'},
                                                            'adresseInstallation': {
                                                                'escalierEtEtageEtAppartement': 'string',
                                                                'batiment': 'string',
                                                                'numeroEtNomVoie': 'string',
                                                                'lieuDit': 'string',
                                                                'codePostal': 'string',
                                                                'commune': {'libelle': 'string', 'code': 'string'}},
                                                            'dateDerniereModificationFormuleTarifaireAcheminement': '2011-09-12',
                                                            'dateDerniereAugmentationPuissanceSouscrite': '2001-09-05',
                                                            'dateDerniereDiminutionPuissanceSouscrite': '2018-10-15',
                                                            'segment': {'libelle': 'string', 'code': 'C3'},
                                                            'niveauOuvertureServices': 'string'},
                                       'situationAlimentation': {
                                           'alimentationPrincipale': {
                                               'domaineTension': {'libelle': 'string', 'code': 'BTSUP'},
                                               'tensionLivraison': {'libelle': 'string', 'code': 'string'},
                                               'modeApresCompteur': {'libelle': 'string', 'code': 'string'},
                                               'puissanceRaccordementSoutirage': {'valeur': 1000.0,
                                                                                  'unite': 'kVAR'}}},
                                       'situationComptage': {
                                           'dispositifComptage': {
                                               'typeComptage': {'libelle': 'string', 'code': 'string'}, 'compteurs': {
                                                   'compteur': [
                                                       {'localisation': {'libelle': 'string', 'code': 'string'},
                                                        'matricule': 'string',
                                                        'ticActivee': True, 'ticStandard': True, 'ticActivable': False,
                                                        'plagesHeuresCreuses': 'string',
                                                        'parametresTeleAcces': {'numeroTelephone': 'string',
                                                                                'numeroVoieAiguillage': 100,
                                                                                'etatLigneTelephonique': 'string',
                                                                                'fenetreEcouteClient': {
                                                                                    'heureDebut': "12:41:25+00:00",
                                                                                    'duree': {'valeur': 1000.0,
                                                                                              'unite': 'annee'}
                                                                                },
                                                                                'cle': 'string'},
                                                        'programmationHoraire': {
                                                            'programmationPosteHoraire': [
                                                                {'libelle': 'string', 'periodesHoraires': 'string',
                                                                 'code': 'string'}]}}]},
                                               'disjoncteur': {'calibre': {'libelle': 'string', 'code': 'string'}},
                                               'relais': {'plageHeuresCreuses': 'string'},
                                               'transformateurCourant': {
                                                   'calibre': {'libelle': 'string', 'code': 'string'},
                                                   'couplage': {'libelle': 'string', 'code': 'string'},
                                                   'classePrecision': {'libelle': 'string',
                                                                       'code': 'string'},
                                                   'position': {'libelle': 'string', 'code': 'string'}},
                                               'transformateurTension': {
                                                   'calibre': {'libelle': 'string', 'code': 'string'},
                                                   'couplage': {'libelle': 'string', 'code': 'string'},
                                                   'classePrecision': {'libelle': 'string',
                                                                       'code': 'string'}}},
                                           'caracteristiquesReleve': {
                                               'modeTraitement': {'libelle': 'string', 'code': 'string'},
                                               'periodicite': {'libelle': 'string', 'code': 'string'},
                                               'plageReleve': {'libelle': 'string', 'code': 'string'}},
                                           'modeReleve': {'libelle': 'string', 'code': 'string'},
                                           'mediaReleve': {'libelle': 'string', 'code': 'string'},
                                           'futuresPlagesHeuresCreuses': {'libelle': 'string', 'code': 'string'},
                                           'futuresProgrammationsHoraires': {
                                               'formuleTarifaireAcheminement': [{'libelle': 'string',
                                                                                 'programmationHoraire': {
                                                                                     'programmationPosteHoraire': [
                                                                                         {'libelle': 'string',
                                                                                          'periodesHoraires': 'string',
                                                                                          'code': 'string'}]},
                                                                                 'code': 'string'}]}},
                                       'situationContractuelle': {
                                           'structureTarifaire': {
                                               'formuleTarifaireAcheminement': {'libelle': 'string', 'code': 'string'},
                                               'longueUtilisation': {
                                                   'contexte': {'libelle': 'string', 'code': 'string'},
                                                   'forfait': {'valeur': 1000.0,
                                                               'unite': 's'}},
                                               'puissanceSouscriteMax': {'valeur': 1000.0,
                                                                         'unite': 'kW'}, 'denivelePuissances': {
                                                   'classesTemporelles': {
                                                       'classeTemporelle': [{'libelle': 'string', 'puissance': {
                                                           'valeur': 1000.0, 'unite': 'kVAR'}, 'code': 'string'}]}},
                                               'calendrierFrn': {'libelle': 'string', 'code': 'string'}}},
                                       'id': 'string'}})

        self.assertEqual(expected_result, reponse.json())