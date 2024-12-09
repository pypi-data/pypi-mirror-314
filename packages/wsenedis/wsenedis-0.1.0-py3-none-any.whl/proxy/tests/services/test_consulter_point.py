import datetime as dt
from _decimal import Decimal
from unittest.mock import patch

import zeep

from enedis.data_models.consulterdonneespoint import DonneesConsulterPoint
from enedis.services.consulter_point import ConsulterPoint
from proxy.tests.services.ServicesTestCase import raise_transport_errror, ServicesTestCase


class TestConsulterPoint(ServicesTestCase):
    maxDiff = None

    expected_response = {'header': {'acquittement': None}, 'body': {'point': {'donneesGenerales': {
        'etatContractuel': {'libelle': 'string', 'code': 'IMPRO'}, 'adresseInstallation':
            {'escalierEtEtageEtAppartement': 'string', 'batiment': 'string',
             'numeroEtNomVoie': 'string', 'lieuDit': 'string', 'codePostal': 'string',
             'commune': {'libelle': 'string', 'code': 'string'}},
        'alimentationComplementaire': False, 'alimentationSecours': False, 'bornePoste':
            True, 'borneFixe': False, 'hebergeurDecomptant': {'libelle': 'string',
                                                              'code': 'DECO'},
        'regroupementTurpe': {'libelle': 'string', 'code': 'NON'},
        'dateDerniereModificationFormuleTarifaireAcheminement': dt.date(2011, 12,
                                                                        4),
        'dateDerniereModificationCalendrierFournisseur': dt.date(2003, 4, 20),
        'dateDerniereModificationGroupePeriodeMobile': dt.date(2014, 12, 2),
        'dateDerniereAugmentationPuissanceSouscrite': dt.date(2012, 7, 23),
        'dateDerniereDiminutionPuissanceSouscrite': dt.date(2010, 7, 29),
        'datePremierePoseCompteurLinky': dt.date(2018, 12, 27), 'segment': {
            'libelle': 'string', 'code': 'C2'}, 'numTelephoneDepannage': 'string',
        'niveauOuvertureServices': 'string', 'sensible': True,
        'autoconsommationIndividuelle': {'libelle': 'string', 'code': 'string'},
        'rattachements': {'rattachement': [{'type': {'libelle': 'string',
                                                     'code': 'string'}, 'dateDebut': dt.date(2006, 3, 19), 'dateFin':
                                                dt.date(2008, 1, 24), 'pointsConfondus': True, 'longueursLiaisons': {
            'longueurLiaisonAerienneHta': {'valeur': Decimal('1000.000000000000000'),
                                           'unite': 'm'}, 'longueurLiaisonSouterraineHta': {'valeur': Decimal(
                '1000.000000000000000'), 'unite': 'km'}}, 'pointsRattaches': {'pointRattache': [{
            'role': {'libelle': 'string', 'code': 'string'}, 'puissanceMaxAppelee': {
                'valeur': Decimal('1000.000000000000000'), 'unite': 'kVA'}, 'finalites': {
                'finalite': [{'libelle': 'string', 'code': 'string'}]}, 'id': 'string'}]}}]}},
        'situationAlimentation': {'etatAlimentation': {'libelle': 'string',
                                                       'code': 'NRAC'},
                                  'alimentationPrincipale': {'domaineTension': {'libelle':
                                                                                    'string', 'code': 'BTSUP'},
                                                             'tensionLivraison': {'libelle': 'string',
                                                                                  'code': 'string'},
                                                             'nbFilsBranchement': 100, 'modeApresCompteur': {'libelle':
                                                                                                                 'string',
                                                                                                             'code': 'string'},
                                                             'longueursLiaisons': {'longueurLiaisonAerienne': {
                                                                 'valeur': Decimal('1000.000000000000000'),
                                                                 'unite': 'km'},
                                                                 'longueurLiaisonSouterraine': {
                                                                     'valeur': Decimal('1000.000000000000000'),
                                                                     'unite': 'm'}},
                                                             'puissanceRaccordementSoutirage': {'valeur': Decimal(
                                                                 '1000.000000000000000'), 'unite': 'kVA'},
                                                             'puissanceLimiteSoutirage': {'valeur':
                                                                 Decimal(
                                                                     '1000.000000000000000'),
                                                                 'unite': 'kWc'},
                                                             'zoneQualiteDesserte': {
                                                                 'libelle': 'string', 'code': 'string'},
                                                             'installationClient': {
                                                                 'nbMoyensProductionAutonome': 100,
                                                                 'puissanceTotaleProductionAutonome': {
                                                                     'valeur': Decimal('1000.000000000000000'),
                                                                     'unite': 'kVA'},
                                                                 'modeCouplageProductionAutonome': {'libelle': 'string',
                                                                                                    'code': 'string'},
                                                                 'dispositifParticulierLimitationPerturbations': 'string'}},
                                  'alimentationsComplementaires': {'alimentationComplementaire': [{
                                      'domaineTension': {'libelle': 'string', 'code': 'BTSUP'}, 'tensionLivraison': {
                                          'libelle': 'string', 'code': 'string'}, 'longueursLiaisons': {
                                          'longueurLiaisonAerienne': {'valeur': Decimal('1000.000000000000000'),
                                                                      'unite': 'm'},
                                          'longueurLiaisonSouterraine': {'valeur': Decimal(
                                              '1000.000000000000000'), 'unite': 'm'}}, 'nbCellules': 100,
                                      'puissanceRaccordementSoutirage': {'valeur': Decimal('1000.000000000000000'),
                                                                         'unite': 'kVAR'}}]},
                                  'alimentationsSecours': {'alimentationSecours': [{
                                      'domaineTension': {'libelle': 'string', 'code': 'HTB'}, 'tensionLivraison': {
                                          'libelle': 'string', 'code': 'string'}, 'longueursLiaisons': {
                                          'longueurLiaisonAerienne': {'valeur': Decimal('1000.000000000000000'),
                                                                      'unite': 'm'},
                                          'longueurLiaisonSouterraine': {'valeur': Decimal(
                                              '1000.000000000000000'), 'unite': 'm'}},
                                      'transformateurDifferentPrincipal':
                                          True, 'puissanceReserveeHt': {'valeur': Decimal('1000.000000000000000'),
                                                                        'unite': 'kWc'},
                                      'puissanceReserveeBt': {'valeur': Decimal(
                                          '1000.000000000000000'), 'unite': 'kW'}, 'modeBasculePrincipaleSecours': {
                                          'libelle': 'string', 'code': 'string'}, 'prorataPuissance': Decimal(
                                          '1000.000000000000000'), 'nbCellules': 100, 'alimentationGarantie': True}]},
                                  'coupure': {'dateDebut': dt.date(2010, 8, 31), 'motif': {'libelle':
                                                                                               'string',
                                                                                           'code': 'string'},
                                              'localisation': {'libelle': 'string',
                                                               'code': 'string'}},
                                  'limitation': {'puissanceLimitee': {'valeur': Decimal(
                                      '1000.000000000000000'), 'unite': 'kVAR'}, 'typeLimiteur': {'libelle': 'string',
                                                                                                  'code': 'string'}}},
        'situationComptage': {'dispositifComptage': {'typeComptage':
                                                         {'libelle': 'string', 'code': 'string'},
                                                     'compteurs': {'compteur': [{
                                                         'numeroSerie': 'string',
                                                         'localisation': {'libelle': 'string', 'code': 'string'},
                                                         'accessibilite': True, 'regimePropriete': {'libelle': 'string',
                                                                                                    'code': 'string'},
                                                         'modeleCompteur': {'typeAppareil': 'string', 'sousType': {
                                                             'libelle': 'string', 'code': 'string'},
                                                                            'anneeFabrication': (2007, None),
                                                                            'nbRoues': 100, 'nbCadrans': 100},
                                                         'matricule': 'string', 'tensionCompteur': {
                                                             'libelle': 'string', 'code': 'string'},
                                                         'puissanceMax': {'valeur': Decimal(
                                                             '1000.000000000000000'), 'unite': 'kVA'},
                                                         'nombreFils': 100, 'intensiteNominale':
                                                             {'libelle': 'string', 'code': 'string'},
                                                         'ticActivee': False, 'ticStandard':
                                                             False, 'ticActivable': True,
                                                         'plagesHeuresCreuses': 'string',
                                                         'periodeDeploiementLinky': 'string',
                                                         'parametresTeleAcces': {'numeroTelephone':
                                                                                     'string',
                                                                                 'numeroVoieAiguillage': 100,
                                                                                 'cle': 'string',
                                                                                 'etatLigneTelephonique':
                                                                                     'string', 'fenetreEcouteClient': {
                                                                 'heureDebut': dt.time(4, 57, 17),
                                                                 'duree': {'valeur': Decimal('1000.000000000000000'),
                                                                           'unite': 's'}}},
                                                         'programmationHoraire': {
                                                             'programmationPosteHoraire': [{'libelle': 'string',
                                                                                            'periodesHoraires': 'string',
                                                                                            'code': 'string'}]},
                                                         'coefficientLecture': Decimal(
                                                             '1000.000000000000000'), 'eligiblePeriodeMobile': False}]},
                                                     'grilleFrn': {
                                                         'calendrier': {'libelle': 'string', 'code': 'string'}},
                                                     'presenceBtr': True,
                                                     'disjoncteur': {
                                                         'localisation': {'libelle': 'string', 'code': 'string'},
                                                         'accessibilite': False,
                                                         'regimePropriete': {'libelle': 'string',
                                                                             'code': 'string'},
                                                         'nature': {'libelle': 'string', 'code': 'string'},
                                                         'intensiteReglage': {'valeur': Decimal('1000.000000000000000'),
                                                                              'unite': 'A'},
                                                         'calibre': {'libelle': 'string', 'code': 'string'},
                                                         'nbPoles': 100}, 'relais': {
                'regimePropriete': {'libelle': 'string', 'code': 'string'}, 'nature': {'libelle':
                                                                                           'string', 'code': 'string'},
                'typeCommande': {'libelle': 'string',
                                 'code': 'string'}, 'plageHeuresCreuses': 'string'}, 'transformateurCourant': {
                'localisation': {'libelle': 'string', 'code': 'string'}, 'accessibilite': False,
                'regimePropriete': {'libelle': 'string', 'code': 'string'}, 'calibre': {
                    'libelle': 'string', 'code': 'string'}, 'couplage': {'libelle': 'string',
                                                                         'code': 'string'},
                'classePrecision': {'libelle': 'string', 'code': 'string'},
                'position': {'libelle': 'string', 'code': 'string'}}, 'transformateurTension': {
                'localisation': {'libelle': 'string', 'code': 'string'}, 'accessibilite': False,
                'regimePropriete': {'libelle': 'string', 'code': 'string'}, 'calibre': {
                    'libelle': 'string', 'code': 'string'}, 'couplage': {'libelle': 'string',
                                                                         'code': 'string'},
                'classePrecision': {'libelle': 'string', 'code': 'string'}},
                                                     'facteurCorrectifPertesJoule': Decimal('1000.000000000000000'),
                                                     'facteurCorrectifPertesFer': Decimal('1000.000000000000000'),
                                                     'facteurCorrectifPertesReactives': Decimal('1000.000000000000000'),
                                                     'particularite': {'libelle': 'string', 'code': 'string'},
                                                     'tensionComptage': {
                                                         'libelle': 'string', 'code': 'string'}},
                              'caracteristiquesReleve': {
                                  'modeTraitement': {'libelle': 'string', 'code': 'string'}, 'periodicite': {
                                      'libelle': 'string', 'code': 'string'}, 'dureeCycle': {'valeur': Decimal(
                                      '1000.000000000000000'), 'unite': 'min'}, 'plageReleve': {'libelle': 'string',
                                                                                                'code': 'string'}},
                              'modeReleve': {'libelle': 'string', 'code': 'string'},
                              'mediaReleve': {'libelle': 'string', 'code': 'string'},
                              'futuresPlagesHeuresCreuses': {'libelle': 'string', 'code': 'string'},
                              'futuresProgrammationsHoraires': {'formuleTarifaireAcheminement': [{'libelle':
                                                                                                      'string',
                                                                                                  'programmationHoraire': {
                                                                                                      'programmationPosteHoraire': [
                                                                                                          {'libelle':
                                                                                                               'string',
                                                                                                           'periodesHoraires': 'string',
                                                                                                           'code': 'string'}]},
                                                                                                  'code': 'string'}]},
                              'teleoperable': True, 'enregistrementCourbeDeCharge': False},
        'situationContractuelle': {'dateDebut': dt.date(2011, 4, 14), 'dateFin':
            dt.date(2003, 8, 19), 'contratId': 'string', 'clientFinal': {'categorie': {
            'libelle': 'string', 'code': 'PRO'}, 'typeResidence': {'libelle': 'string',
                                                                   'code': 'SEC'}, 'refFournisseur': 'string',
            'personnePhysique': {'civilite':
                                     'string', 'nom': 'string', 'prenom': 'string'}, 'personneMorale': None,
            'adressePostale': {'ligne1': 'string', 'ligne2': 'string', 'ligne3': 'string',
                               'ligne4': 'string', 'ligne5': 'string', 'ligne6': 'string', 'ligne7': 'string'},
            'coordonneesContact': {'numTelephone1': 'string', 'numTelephone2': 'string',
                                   'numFax': 'string', 'adresseEmail': 'string'}}, 'interlocuteurClient': {
            'personnePhysique': {'civilite': 'string', 'nom': 'string', 'prenom': 'string'},
            'personneMorale': None, 'adressePostale': {'ligne1': 'string', 'ligne2':
                'string', 'ligne3': 'string', 'ligne4': 'string', 'ligne5': 'string',
                                                       'ligne6': 'string', 'ligne7': 'string'},
            'coordonneesContact': {'numTelephone1':
                                       'string', 'numTelephone2': 'string', 'numFax': 'string', 'adresseEmail':
                                       'string'}}, 'interlocuteurTechnique': {'personnePhysique': {'civilite': 'string',
                                                                                                   'nom': 'string',
                                                                                                   'prenom': 'string'},
                                                                              'personneMorale': None,
                                                                              'adressePostale': {
                                                                                  'ligne1': 'string',
                                                                                  'ligne2': 'string',
                                                                                  'ligne3': 'string',
                                                                                  'ligne4': 'string',
                                                                                  'ligne5': 'string',
                                                                                  'ligne6': 'string',
                                                                                  'ligne7': 'string'},
                                                                              'coordonneesContact': {
                                                                                  'numTelephone1': 'string',
                                                                                  'numTelephone2': 'string',
                                                                                  'numFax': 'string',
                                                                                  'adresseEmail': 'string'}},
                                   'structureTarifaire': {
                                       'formuleTarifaireAcheminement': {'libelle': 'string', 'code': 'string'},
                                       'longueUtilisation': {'contexte': {'libelle': 'string', 'code': 'string'},
                                                             'forfait': {'valeur': Decimal('1000.000000000000000'),
                                                                         'unite': 'jour'}},
                                       'codeTarifAcheminement': 'string', 'puissanceSouscriteMax': {'valeur': Decimal(
                                           '1000.000000000000000'), 'unite': 'kW'}, 'denivelePuissances': {
                                           'classesTemporelles': {
                                               'classeTemporelle': [{'libelle': 'string', 'puissance': {
                                                   'valeur': Decimal('1000.000000000000000'), 'unite': 'kVAR'},
                                                                     'code': 'string'}]}},
                                       'calendrierFrn': {'libelle': 'string', 'code': 'string'},
                                       'groupePeriodeMobile': {'libelle': 'string', 'code': 'string'}}, 'siContractuel':
                                       {'libelle': 'string', 'code': 'string'}}, 'optionsContractuellesSouscrites': {
            'engagementQualiteFourniture': [{'dateSouscription': dt.date(2011, 7, 22),
                                             'dateResiliation': dt.date(2004, 3, 3), 'dureeCreux': {'valeur': Decimal(
                    '1000.000000000000000'), 'unite': 'jour'}, 'periodicite': {'libelle': 'string',
                                                                               'code': 'string'}, 'nbCreux': 100,
                                             'profondeurCreux': Decimal(
                                                 '1000.000000000000000'), 'dateReferenceCreux': dt.date(2017, 8, 12),
                                             'id': 201}], 'telecommandeInterrupteurs': [{'dateSouscription': dt.date(
                2009, 7, 12), 'dateResiliation': dt.date(2018, 8, 2), 'nbDirections':
                100}], 'protectionsChantier': [{'dateSouscription': dt.date(2001, 10, 24),
                                                'dateResiliation': dt.date(2001, 2, 20), 'nbPortees': 100}],
            'courbesCharge': [{'dateSouscription': dt.date(2017, 9, 14),
                               'dateResiliation': dt.date(2008, 4, 17), 'transmission': True,
                               'utilisationRecoflux': False, 'periodicite': {'valeur': Decimal(
                    '1000.000000000000000'), 'unite': 'min'}, 'pasCourbeCharge': {'valeur': Decimal(
                    '1000.000000000000000'), 'unite': 'jour'}}], 'engagementContinuiteFourniture': [{
                'dateSouscription': dt.date(2007, 5, 31), 'dateResiliation': dt.date(
                    2012, 3, 23), 'type': {'libelle': 'string', 'code': 'string'}, 'periodicite': {
                    'libelle': 'string', 'code': 'string'}, 'typesCoupures': {'libelle': 'string',
                                                                              'code': 'string'},
                'nbCoupuresBreves': 100, 'nbCoupuresLongues': 100,
                'nbTotalCoupures': 100, 'dateReferenceCoupures': dt.date(2014, 12, 18),
                'id': 201}], 'periodeObservation': [{'dateSouscription': dt.date(2005, 9,
                                                                                 5),
                                                     'dateResiliation': dt.date(2010, 2, 23),
                                                     'duree': {'valeur': Decimal(
                                                         '1000.000000000000000'), 'unite': 'semaine'}}],
            'calendrierFournisseur': [{
                'dateSouscription': dt.date(2013, 10, 31), 'dateResiliation':
                    dt.date(2018, 8, 10), 'calendrier': {'libelle': 'string',
                                                         'code': 'string'}, 'profilable': False,
                'periodeMobileAutorisee': False}]},
        'modificationsContractuellesEnCours': {'modificationContractuelleEnCours': [{
            'prestations': {'prestation': [{'fiche': {'libelle': 'string', 'code': 'string'},
                                            'option': {'libelle': 'string', 'code': 'string'},
                                            'cas': {'libelle': 'string',
                                                    'code': 'string'}, 'rang': 100,
                                            'dateEffetReelle': dt.date(2019, 3, 30),
                                            'dateEffetPrevue': dt.date(2001, 9, 30)}]}, 'demande': {'contratId':
                                                                                                        'string',
                                                                                                    'dateEffetSouhaitee': dt.date(
                                                                                                        2003, 7, 15),
                                                                                                    'clientFinal': {
                                                                                                        'categorie': {
                                                                                                            'libelle': 'string',
                                                                                                            'code': 'RES'},
                                                                                                        'typeResidence': {
                                                                                                            'libelle':
                                                                                                                'string',
                                                                                                            'code': 'PRP'},
                                                                                                        'refFournisseur': 'string',
                                                                                                        'personnePhysique': {
                                                                                                            'civilite': 'string',
                                                                                                            'nom': 'string',
                                                                                                            'prenom': 'string'},
                                                                                                        'personneMorale':
                                                                                                            None,
                                                                                                        'adressePostale': {
                                                                                                            'ligne1': 'string',
                                                                                                            'ligne2': 'string',
                                                                                                            'ligne3': 'string',
                                                                                                            'ligne4': 'string',
                                                                                                            'ligne5': 'string',
                                                                                                            'ligne6': 'string',
                                                                                                            'ligne7': 'string'},
                                                                                                        'coordonneesContact': {
                                                                                                            'numTelephone1': 'string',
                                                                                                            'numTelephone2': 'string',
                                                                                                            'numFax': 'string',
                                                                                                            'adresseEmail': 'string'}},
                                                                                                    'structureTarifaire': {
                                                                                                        'formuleTarifaireAcheminement': {
                                                                                                            'libelle': 'string',
                                                                                                            'code': 'string'},
                                                                                                        'longueUtilisation': {
                                                                                                            'contexte': {
                                                                                                                'libelle': 'string',
                                                                                                                'code': 'string'},
                                                                                                            'forfait': {
                                                                                                                'valeur': Decimal(
                                                                                                                    '1000.000000000000000'),
                                                                                                                'unite': 'ms'}},
                                                                                                        'codeTarifAcheminement': 'string',
                                                                                                        'puissanceSouscriteMax': {
                                                                                                            'valeur': Decimal(
                                                                                                                '1000.000000000000000'),
                                                                                                            'unite': 'kW'},
                                                                                                        'denivelePuissances':
                                                                                                            {
                                                                                                                'classesTemporelles': {
                                                                                                                    'classeTemporelle': [
                                                                                                                        {
                                                                                                                            'libelle': 'string',
                                                                                                                            'puissance': {
                                                                                                                                'valeur': Decimal(
                                                                                                                                    '1000.000000000000000'),
                                                                                                                                'unite': 'kVAR'},
                                                                                                                            'code': 'string'}]}},
                                                                                                        'calendrierFrn': {
                                                                                                            'libelle': 'string',
                                                                                                            'code': 'string'},
                                                                                                        'groupePeriodeMobile': {
                                                                                                            'libelle': 'string',
                                                                                                            'code': 'string'}}},
            'affaireId':
                'string'}]}, 'interventionsEnCours': {'interventionEnCours': [{'affaireId': [
            'string'], 'teleoperable': False, 'operations': {'operation': [{'libelle':
                                                                                'string', 'code': 'string'}],
                                                             'referencesDisco': {'objet': {'libelle': 'string',
                                                                                           'code': 'string'},
                                                                                 'nature': {'libelle': 'string',
                                                                                            'code': 'string'}}},
            'dateCreationAc': dt.date(2012, 5, 17), 'datePrevue': dt.date(2001,
                                                                          6, 26), 'heureDebut': dt.time(7, 28, 19),
            'heureFin': dt.time(13, 49,
                                34), 'creneauHorairePrevu': {'libelle': 'string', 'code': 'string'}}]},
        'historiqueAffaires': {'affaire': [{'prestation': {'fiche': {'libelle': 'string',
                                                                     'code': 'string'},
                                                           'option': {'libelle': 'string', 'code': 'string'},
                                                           'cas': {'libelle': 'string', 'code': 'string'}, 'rang': 100},
                                            'refFournisseur':
                                                'string', 'client': 'string',
                                            'nomCommercialActeurMarcheInitiateur': 'string',
                                            'dateEnvoi': dt.date(2005, 3, 29), 'dateEffet': dt.date(2003, 6, 10),
                                            'loginInitiateur': 'string',
                                            'etat': {'libelle': 'string', 'code': 'string'},
                                            'motifCloture': {'libelle': 'string', 'code': 'string'},
                                            'statut': {'libelle':
                                                           'string', 'code': 'ANNUL'}, 'id': 'string'}]},
        'elementsProchainesMesures': {
            'prochainCalculConsommation': {'nature': {'libelle': 'string', 'code': 'string'},
                                           'dateTheoriqueProchainCalculConsommation': dt.date(2015, 12, 31)},
            'dateTheoriqueProchainReleve': dt.date(2013, 9, 16)},
        'derniersIndexPublies': {'date': dt.date(2013, 10, 24), 'declencheur': {
            'libelle': 'string', 'code': 'string'}, 'nature': {'libelle': 'string',
                                                               'code': 'string'},
                                 'origine': {'libelle': 'string', 'code': 'string'},
                                 'grilleTurpe': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                                 'classesTemporelles': {
                                                     'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                         'valeur': Decimal('1000.000000000000000'), 'unite': 'string',
                                                         'grandeurPhysique':
                                                             {'libelle': 'string', 'code': 'string'}, 'phase': 100}],
                                                                           'code': 'string'}]}},
                                 'grilleFrn': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                               'classesTemporelles': {
                                                   'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                       'valeur': Decimal('1000.000000000000000'), 'unite': 'string',
                                                       'grandeurPhysique':
                                                           {'libelle': 'string', 'code': 'string'}, 'phase': 100}],
                                                                         'code': 'string'}]}}},
        'derniersIndexReleves': {'date': dt.date(2000, 9, 30), 'declencheur': {
            'libelle': 'string', 'code': 'string'}, 'nature': {'libelle': 'string',
                                                               'code': 'string'},
                                 'origine': {'libelle': 'string', 'code': 'string'},
                                 'grilleTurpe': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                                 'classesTemporelles': {
                                                     'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                         'valeur': Decimal('1000.000000000000000'), 'unite': 'string',
                                                         'grandeurPhysique':
                                                             {'libelle': 'string', 'code': 'string'}, 'phase': 100}],
                                                                           'code': 'string'}]}},
                                 'grilleFrn': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                               'classesTemporelles': {
                                                   'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                       'valeur': Decimal('1000.000000000000000'), 'unite': 'string',
                                                       'grandeurPhysique':
                                                           {'libelle': 'string', 'code': 'string'}, 'phase': 100}],
                                                                         'code': 'string'}]}}},
        'id': 'string'}}}

    def test_creation_message_correct(self):
        donnees = DonneesConsulterPoint('12345678911234')
        msg, _ = ConsulterPoint.consulter_donnees_point(self.connection, donnees, send=False)

        expected_msg = {
            'autorisationClient': True,
            'contratConcluNouveauClientSurSite': None,
            'donneesDemandees': {
                'donneesGeneralesPoint': True,
                'modificationsContractuellesEnCours': True,
                'interventionsEnCours': True,
                'historiqueAffaires': True,
                'elementsProchainesMesures': True,
                'derniersIndex': True
            },
            'pointId': '12345678911234',
            'loginUtilisateur': 'test@test.fr'}
        self.assertDictEqual(msg, expected_msg)

    def test_creation_message_mauvais_type_d_entree(self):
        donnees = DonneesConsulterPoint('12345678911234', donnees_generales=None)
        _, response = ConsulterPoint.consulter_donnees_point(self.connection, donnees)
        self.assertEqual(response['erreur'], "('Missing element donneesGeneralesPoint',)")

    @patch.object(zeep.helpers, 'serialize_object', raise_transport_errror)
    def test_connexion_echoue(self):
        donnees = DonneesConsulterPoint('12345678911234')
        _, response = ConsulterPoint.consulter_donnees_point(self.connection, donnees)
        self.assertEqual(response, {'erreur': "('une erreur inconnue est survenue',)", 'status': 'failed'})

    def test_connexion(self):
        donnees = DonneesConsulterPoint('12345678911234')
        _, response = ConsulterPoint.consulter_donnees_point(self.connection, donnees)

        self.assertDictEqual(response, self.expected_response)
