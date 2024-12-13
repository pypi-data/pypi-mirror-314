import datetime as dt
import decimal
from pprint import pprint
from unittest.mock import patch

import pytz
import zeep
from dateutil import tz
from zeep.helpers import serialize_object

from enedis.data_models.consulterdonneestechniquescontractuelles import ConsulterDonneesTechniquesContractuelles
from enedis.services.consulter_donnees_techniques_contractuelles import ConsulterDoneesTechniquesContractuelles
from proxy.tests.services.ServicesTestCase import ServicesTestCase, raise_transport_errror, raise_creation_error


def normalize_to_utc(dt):
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(pytz.UTC)

def normalize_dict_timezones(d):
    if isinstance(d, dict):
        return {k: normalize_dict_timezones(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [normalize_dict_timezones(x) for x in d]
    elif isinstance(d, dt.datetime):
        return normalize_to_utc(d)
    elif isinstance(d, dt.time):
        _dt = dt.datetime.combine(dt.date.today(), d)
        utc_dt = _dt.astimezone(tz.gettz('UTC')) if _dt.tzinfo else _dt
        return utc_dt.time()
    else:
        return d

def convert_decimal_to_float(d):
    if isinstance(d, dict):
        return {k: convert_decimal_to_float(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_decimal_to_float(x) for x in d]
    elif isinstance(d, decimal.Decimal):
        return float(d)
    else:
        return d

class TestConsulterDonneesTechniquesContractuelles(ServicesTestCase):
    maxDiff = None

    def test_creation_message_correct(self):
        donnees = ConsulterDonneesTechniquesContractuelles('12345678901234', autorisation_client=True)
        msg, _ = ConsulterDoneesTechniquesContractuelles.consultation_donnees_techniques_contractuelles(self.connection, donnees, send=False)
        expected_message = {'pointId': '12345678901234', 'loginUtilisateur': 'test@test.fr', 'autorisationClient': True}
        self.assertDictEqual(msg, expected_message)

    def test_connexion(self):
        donnees = ConsulterDonneesTechniquesContractuelles('12345678901234', autorisation_client=True)

        msg, response = ConsulterDoneesTechniquesContractuelles.consultation_donnees_techniques_contractuelles(self.connection, donnees)

        expected_response = dict(header={'acquittement': None},
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
                                                            'dateDerniereModificationFormuleTarifaireAcheminement': dt.date(
                                                                2011, 9, 12),
                                                            'dateDerniereAugmentationPuissanceSouscrite': dt.date(2001,
                                                                                                                  9, 5),
                                                            'dateDerniereDiminutionPuissanceSouscrite': dt.date(2018,
                                                                                                                10, 15),
                                                            'segment': {'libelle': 'string', 'code': 'C3'},
                                                            'niveauOuvertureServices': 'string'},
                                       'situationAlimentation': {
                                           'alimentationPrincipale': {
                                               'domaineTension': {'libelle': 'string', 'code': 'BTSUP'},
                                               'tensionLivraison': {'libelle': 'string', 'code': 'string'},
                                               'modeApresCompteur': {'libelle': 'string', 'code': 'string'},
                                               'puissanceRaccordementSoutirage': {'valeur': 1000.,
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
                                                                                    'heureDebut': dt.time(12, 41, 25),
                                                                                    'duree': {'valeur': 1000.,
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
                                                   'forfait': {'valeur': 1000.,
                                                               'unite': 's'}},
                                               'puissanceSouscriteMax': {'valeur': 1000.,
                                                                         'unite': 'kW'}, 'denivelePuissances': {
                                                   'classesTemporelles': {
                                                       'classeTemporelle': [{'libelle': 'string', 'puissance': {
                                                           'valeur': 1000., 'unite': 'kVAR'}, 'code': 'string'}]}},
                                               'calendrierFrn': {'libelle': 'string', 'code': 'string'}}},
                                       'id': 'string'}})

        response = convert_decimal_to_float(response)
        response = normalize_dict_timezones(response)
        self.assertDictEqual(response, expected_response)

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        donnees = ConsulterDonneesTechniquesContractuelles('12345678901234', autorisation_client=True)

        msg, response = ConsulterDoneesTechniquesContractuelles.consultation_donnees_techniques_contractuelles(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})



