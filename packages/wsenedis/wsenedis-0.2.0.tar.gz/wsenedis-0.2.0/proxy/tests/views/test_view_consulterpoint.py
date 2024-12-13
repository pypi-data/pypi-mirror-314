
from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.consulterdonneespoint import DonneesConsulterPoint


class TestViewConsulterPoint(TestCase):
    maxDiff = None

    def test_view_consulterpoint(self):
        client = APIClient()
        donnees = DonneesConsulterPoint('12345678911234', autorisation_client=True)
        entree = {'serveur': 'poste_travail', 'donnees': donnees}
        reponse = client.post('/ws/v4.0/consulterpoint/', entree, format='json')
        resultat_attendu = {'header': {'acquittement': None}, 'body': {'point': {'donneesGenerales': {
            'etatContractuel': {'libelle': 'string', 'code': 'IMPRO'}, 'adresseInstallation':
                {'escalierEtEtageEtAppartement': 'string', 'batiment': 'string',
                 'numeroEtNomVoie': 'string', 'lieuDit': 'string', 'codePostal': 'string',
                 'commune': {'libelle': 'string', 'code': 'string'}},
            'alimentationComplementaire': False, 'alimentationSecours': False, 'bornePoste':
                True, 'borneFixe': False, 'hebergeurDecomptant': {'libelle': 'string',
                                                                  'code': 'DECO'},
            'regroupementTurpe': {'libelle': 'string', 'code': 'NON'},
            'dateDerniereModificationFormuleTarifaireAcheminement': '2011-12-04',
            'dateDerniereModificationCalendrierFournisseur': '2003-04-20',
            'dateDerniereModificationGroupePeriodeMobile': '2014-12-02',
            'dateDerniereAugmentationPuissanceSouscrite': '2012-07-23',
            'dateDerniereDiminutionPuissanceSouscrite': '2010-07-29',
            'datePremierePoseCompteurLinky': '2018-12-27', 'segment': {
                'libelle': 'string', 'code': 'C2'}, 'numTelephoneDepannage': 'string',
            'niveauOuvertureServices': 'string', 'sensible': True,
            'autoconsommationIndividuelle': {'libelle': 'string', 'code': 'string'},
            'rattachements': {'rattachement': [{'type': {'libelle': 'string',
                                                         'code': 'string'}, 'dateDebut': '2006-03-19',
                                                'dateFin':
                                                    '2008-01-24', 'pointsConfondus': True,
                                                'longueursLiaisons': {
                                                    'longueurLiaisonAerienneHta': {
                                                        'valeur': 1000.0,
                                                        'unite': 'm'},
                                                    'longueurLiaisonSouterraineHta': {'valeur': 1000.0, 'unite': 'km'}},
                                                'pointsRattaches': {'pointRattache': [{
                                                    'role': {'libelle': 'string', 'code': 'string'},
                                                    'puissanceMaxAppelee': {
                                                        'valeur': 1000.0, 'unite': 'kVA'},
                                                    'finalites': {
                                                        'finalite': [{'libelle': 'string', 'code': 'string'}]},
                                                    'id': 'string'}]}}]}},
            'situationAlimentation': {'etatAlimentation': {'libelle': 'string',
                                                           'code': 'NRAC'},
                                      'alimentationPrincipale': {'domaineTension': {'libelle':
                                                                                        'string', 'code': 'BTSUP'},
                                                                 'tensionLivraison': {'libelle': 'string',
                                                                                      'code': 'string'},
                                                                 'nbFilsBranchement': 100,
                                                                 'modeApresCompteur': {'libelle':
                                                                                           'string', 'code': 'string'},
                                                                 'longueursLiaisons': {'longueurLiaisonAerienne': {
                                                                     'valeur': 1000.0,
                                                                     'unite': 'km'},
                                                                     'longueurLiaisonSouterraine': {
                                                                         'valeur': 1000.0,
                                                                         'unite': 'm'}},
                                                                 'puissanceRaccordementSoutirage': {'valeur': 1000.0, 'unite': 'kVA'},
                                                                 'puissanceLimiteSoutirage': {'valeur':
                                                                                                  1000.0,
                                                                                              'unite': 'kWc'},
                                                                 'zoneQualiteDesserte': {
                                                                     'libelle': 'string', 'code': 'string'},
                                                                 'installationClient': {
                                                                     'nbMoyensProductionAutonome': 100,
                                                                     'puissanceTotaleProductionAutonome': {
                                                                         'valeur': 1000.0,
                                                                         'unite': 'kVA'},
                                                                     'modeCouplageProductionAutonome': {
                                                                         'libelle': 'string', 'code': 'string'},
                                                                     'dispositifParticulierLimitationPerturbations': 'string'}},
                                      'alimentationsComplementaires': {'alimentationComplementaire': [{
                                          'domaineTension': {'libelle': 'string', 'code': 'BTSUP'},
                                          'tensionLivraison': {
                                              'libelle': 'string', 'code': 'string'}, 'longueursLiaisons': {
                                              'longueurLiaisonAerienne': {'valeur': 1000.0,
                                                                          'unite': 'm'},
                                              'longueurLiaisonSouterraine': {'valeur': 1000.0, 'unite': 'm'}}, 'nbCellules': 100,
                                          'puissanceRaccordementSoutirage': {'valeur': 1000.0,
                                                                             'unite': 'kVAR'}}]},
                                      'alimentationsSecours': {'alimentationSecours': [{
                                          'domaineTension': {'libelle': 'string', 'code': 'HTB'}, 'tensionLivraison': {
                                              'libelle': 'string', 'code': 'string'}, 'longueursLiaisons': {
                                              'longueurLiaisonAerienne': {'valeur': 1000.0,
                                                                          'unite': 'm'},
                                              'longueurLiaisonSouterraine': {'valeur': 1000.0, 'unite': 'm'}},
                                          'transformateurDifferentPrincipal':
                                              True, 'puissanceReserveeHt': {'valeur': 1000.0,
                                                                            'unite': 'kWc'},
                                          'puissanceReserveeBt': {'valeur': 1000.0, 'unite': 'kW'}, 'modeBasculePrincipaleSecours': {
                                              'libelle': 'string', 'code': 'string'}, 'prorataPuissance': 1000.0, 'nbCellules': 100,
                                          'alimentationGarantie': True}]},
                                      'coupure': {'dateDebut': '2010-08-31', 'motif': {'libelle':
                                                                                                   'string',
                                                                                               'code': 'string'},
                                                  'localisation': {'libelle': 'string',
                                                                   'code': 'string'}},
                                      'limitation': {'puissanceLimitee': {'valeur': 1000.0, 'unite': 'kVAR'},
                                          'typeLimiteur': {'libelle': 'string',
                                                           'code': 'string'}}},
            'situationComptage': {'dispositifComptage': {'typeComptage':
                                                             {'libelle': 'string', 'code': 'string'},
                                                         'compteurs': {'compteur': [{
                                                             'numeroSerie': 'string',
                                                             'localisation': {'libelle': 'string', 'code': 'string'},
                                                             'accessibilite': True,
                                                             'regimePropriete': {'libelle': 'string',
                                                                                 'code': 'string'},
                                                             'modeleCompteur': {'typeAppareil': 'string', 'sousType': {
                                                                 'libelle': 'string', 'code': 'string'},
                                                                                'anneeFabrication': [2007, None],
                                                                                'nbRoues': 100, 'nbCadrans': 100},
                                                             'matricule': 'string', 'tensionCompteur': {
                                                                 'libelle': 'string', 'code': 'string'},
                                                             'puissanceMax': {'valeur': 1000.0, 'unite': 'kVA'},
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
                                                                                         'string',
                                                                                     'fenetreEcouteClient': {
                                                                                         'heureDebut': '04:57:17',
                                                                                         'duree': {'valeur': 1000.0,
                                                                                                   'unite': 's'}}},
                                                             'programmationHoraire': {
                                                                 'programmationPosteHoraire': [{'libelle': 'string',
                                                                                                'periodesHoraires': 'string',
                                                                                                'code': 'string'}]},
                                                             'coefficientLecture': 1000.0,
                                                             'eligiblePeriodeMobile': False}]}, 'grilleFrn': {
                    'calendrier': {'libelle': 'string', 'code': 'string'}}, 'presenceBtr': True,
                                                         'disjoncteur': {
                                                             'localisation': {'libelle': 'string', 'code': 'string'},
                                                             'accessibilite': False,
                                                             'regimePropriete': {'libelle': 'string',
                                                                                 'code': 'string'},
                                                             'nature': {'libelle': 'string', 'code': 'string'},
                                                             'intensiteReglage': {
                                                                 'valeur': 1000.0,
                                                                 'unite': 'A'},
                                                             'calibre': {'libelle': 'string', 'code': 'string'},
                                                             'nbPoles': 100}, 'relais': {
                    'regimePropriete': {'libelle': 'string', 'code': 'string'}, 'nature': {'libelle':
                                                                                               'string',
                                                                                           'code': 'string'},
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
                                                         'facteurCorrectifPertesJoule': 1000.0,
                                                         'facteurCorrectifPertesFer': 1000.0,
                                                         'facteurCorrectifPertesReactives': 1000.0,
                                                         'particularite': {'libelle': 'string', 'code': 'string'},
                                                         'tensionComptage': {
                                                             'libelle': 'string', 'code': 'string'}},
                                  'caracteristiquesReleve': {
                                      'modeTraitement': {'libelle': 'string', 'code': 'string'}, 'periodicite': {
                                          'libelle': 'string', 'code': 'string'}, 'dureeCycle': {'valeur': 1000.0,
                                                                                                 'unite': 'min'}, 'plageReleve': {'libelle': 'string',
                                                                                                    'code': 'string'}},
                                  'modeReleve': {'libelle': 'string', 'code': 'string'},
                                  'mediaReleve': {'libelle': 'string', 'code': 'string'},
                                  'futuresPlagesHeuresCreuses': {'libelle': 'string', 'code': 'string'},
                                  'futuresProgrammationsHoraires': {'formuleTarifaireAcheminement': [{'libelle':
                                                                                                          'string',
                                                                                                      'programmationHoraire': {
                                                                                                          'programmationPosteHoraire': [
                                                                                                              {
                                                                                                                  'libelle':
                                                                                                                      'string',
                                                                                                                  'periodesHoraires': 'string',
                                                                                                                  'code': 'string'}]},
                                                                                                      'code': 'string'}]},
                                  'teleoperable': True, 'enregistrementCourbeDeCharge': False},
            'situationContractuelle': {'dateDebut': '2011-04-14', 'dateFin':
                '2003-08-19', 'contratId': 'string', 'clientFinal': {'categorie': {
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
                                           'string'}},
                                       'interlocuteurTechnique': {'personnePhysique': {'civilite': 'string',
                                                                                       'nom': 'string',
                                                                                       'prenom': 'string'},
                                                                  'personneMorale': None, 'adressePostale': {
                                               'ligne1': 'string', 'ligne2': 'string', 'ligne3': 'string',
                                               'ligne4': 'string',
                                               'ligne5': 'string', 'ligne6': 'string', 'ligne7': 'string'},
                                                                  'coordonneesContact': {'numTelephone1': 'string',
                                                                                         'numTelephone2': 'string',
                                                                                         'numFax': 'string',
                                                                                         'adresseEmail': 'string'}},
                                       'structureTarifaire': {
                                           'formuleTarifaireAcheminement': {'libelle': 'string', 'code': 'string'},
                                           'longueUtilisation': {'contexte': {'libelle': 'string', 'code': 'string'},
                                                                 'forfait': {'valeur': 1000.0,
                                                                             'unite': 'jour'}},
                                           'codeTarifAcheminement': 'string',
                                           'puissanceSouscriteMax': {'valeur': 1000.0, 'unite': 'kW'},
                                           'denivelePuissances': {
                                               'classesTemporelles': {
                                                   'classeTemporelle': [{'libelle': 'string', 'puissance': {
                                                       'valeur': 1000.0, 'unite': 'kVAR'},
                                                                         'code': 'string'}]}},
                                           'calendrierFrn': {'libelle': 'string', 'code': 'string'},
                                           'groupePeriodeMobile': {'libelle': 'string', 'code': 'string'}},
                                       'siContractuel':
                                           {'libelle': 'string', 'code': 'string'}},
            'optionsContractuellesSouscrites': {
                'engagementQualiteFourniture': [{'dateSouscription': '2011-07-22',
                                                 'dateResiliation': '2004-03-03',
                                                 'dureeCreux': {'valeur': 1000.0, 'unite': 'jour'},
                                                 'periodicite': {'libelle': 'string',
                                                                 'code': 'string'}, 'nbCreux': 100,
                                                 'profondeurCreux': 1000.0,
                                                 'dateReferenceCreux': '2017-08-12',
                                                 'id': 201}],
                'telecommandeInterrupteurs': [{'dateSouscription': '2009-07-12', 'dateResiliation': '2018-08-02', 'nbDirections':
                    100}], 'protectionsChantier': [{'dateSouscription': '2001-10-24',
                                                    'dateResiliation': '2001-02-20', 'nbPortees': 100}],
                'courbesCharge': [{'dateSouscription': '2017-09-14',
                                   'dateResiliation': '2008-04-17', 'transmission': True,
                                   'utilisationRecoflux': False, 'periodicite': {'valeur': 1000.0,
                                                                                 'unite': 'min'},
                                   'pasCourbeCharge': {'valeur': 1000.0, 'unite': 'jour'}}], 'engagementContinuiteFourniture': [{
                    'dateSouscription': '2007-05-31', 'dateResiliation': '2012-03-23',
                    'type': {'libelle': 'string', 'code': 'string'}, 'periodicite': {
                        'libelle': 'string', 'code': 'string'}, 'typesCoupures': {'libelle': 'string',
                                                                                  'code': 'string'},
                    'nbCoupuresBreves': 100, 'nbCoupuresLongues': 100,
                    'nbTotalCoupures': 100, 'dateReferenceCoupures': '2014-12-18',
                    'id': 201}], 'periodeObservation': [{'dateSouscription': '2005-09-05',
                                                         'dateResiliation': '2010-02-23',
                                                         'duree': {'valeur': 1000.0, 'unite': 'semaine'}}],
                'calendrierFournisseur': [{
                    'dateSouscription': '2013-10-31', 'dateResiliation':
                        '2018-08-10', 'calendrier': {'libelle': 'string',
                                                             'code': 'string'}, 'profilable': False,
                    'periodeMobileAutorisee': False}]},
            'modificationsContractuellesEnCours': {'modificationContractuelleEnCours': [{
                'prestations': {'prestation': [{'fiche': {'libelle': 'string', 'code': 'string'},
                                                'option': {'libelle': 'string', 'code': 'string'},
                                                'cas': {'libelle': 'string',
                                                        'code': 'string'}, 'rang': 100,
                                                'dateEffetReelle': '2019-03-30',
                                                'dateEffetPrevue': '2001-09-30'}]}, 'demande': {'contratId':
                                                                                                            'string',
                                                                                                        'dateEffetSouhaitee': '2003-07-15',
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
                                                                                                                    'valeur': 1000.0,
                                                                                                                    'unite': 'ms'}},
                                                                                                            'codeTarifAcheminement': 'string',
                                                                                                            'puissanceSouscriteMax': {
                                                                                                                'valeur': 1000.0,
                                                                                                                'unite': 'kW'},
                                                                                                            'denivelePuissances':
                                                                                                                {
                                                                                                                    'classesTemporelles': {
                                                                                                                        'classeTemporelle': [
                                                                                                                            {
                                                                                                                                'libelle': 'string',
                                                                                                                                'puissance': {
                                                                                                                                    'valeur': 1000.0,
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
                'dateCreationAc': '2012-05-17', 'datePrevue': '2001-06-26', 'heureDebut': '07:28:19',
                'heureFin': '13:49:34', 'creneauHorairePrevu': {'libelle': 'string', 'code': 'string'}}]},
            'historiqueAffaires': {'affaire': [{'prestation': {'fiche': {'libelle': 'string',
                                                                         'code': 'string'},
                                                               'option': {'libelle': 'string', 'code': 'string'},
                                                               'cas': {'libelle': 'string', 'code': 'string'},
                                                               'rang': 100}, 'refFournisseur':
                                                    'string', 'client': 'string',
                                                'nomCommercialActeurMarcheInitiateur': 'string',
                                                'dateEnvoi': '2005-03-29', 'dateEffet': '2003-06-10',
                                                'loginInitiateur': 'string',
                                                'etat': {'libelle': 'string', 'code': 'string'},
                                                'motifCloture': {'libelle': 'string', 'code': 'string'},
                                                'statut': {'libelle':
                                                               'string', 'code': 'ANNUL'}, 'id': 'string'}]},
            'elementsProchainesMesures': {
                'prochainCalculConsommation': {'nature': {'libelle': 'string', 'code': 'string'},
                                               'dateTheoriqueProchainCalculConsommation': '2015-12-31'},
                'dateTheoriqueProchainReleve': '2013-09-16'},
            'derniersIndexPublies': {'date': '2013-10-24', 'declencheur': {
                'libelle': 'string', 'code': 'string'}, 'nature': {'libelle': 'string',
                                                                   'code': 'string'},
                                     'origine': {'libelle': 'string', 'code': 'string'},
                                     'grilleTurpe': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                                     'classesTemporelles': {
                                                         'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                             'valeur': 1000.0,
                                                             'unite': 'string', 'grandeurPhysique':
                                                                 {'libelle': 'string', 'code': 'string'},
                                                             'phase': 100}], 'code': 'string'}]}},
                                     'grilleFrn': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                                   'classesTemporelles': {
                                                       'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                           'valeur': 1000.0, 'unite': 'string',
                                                           'grandeurPhysique':
                                                               {'libelle': 'string', 'code': 'string'}, 'phase': 100}],
                                                                             'code': 'string'}]}}},
            'derniersIndexReleves': {'date': '2000-09-30', 'declencheur': {
                'libelle': 'string', 'code': 'string'}, 'nature': {'libelle': 'string',
                                                                   'code': 'string'},
                                     'origine': {'libelle': 'string', 'code': 'string'},
                                     'grilleTurpe': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                                     'classesTemporelles': {
                                                         'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                             'valeur': 1000.0,
                                                             'unite': 'string', 'grandeurPhysique':
                                                                 {'libelle': 'string', 'code': 'string'},
                                                             'phase': 100}], 'code': 'string'}]}},
                                     'grilleFrn': {'calendrier': {'libelle': 'string', 'code': 'string'},
                                                   'classesTemporelles': {
                                                       'classeTemporelle': [{'libelle': 'string', 'index': [{
                                                           'valeur': 1000.0, 'unite': 'string',
                                                           'grandeurPhysique':
                                                               {'libelle': 'string', 'code': 'string'}, 'phase': 100}],
                                                                             'code': 'string'}]}}},
            'id': 'string'}}}

        self.assertDictEqual(reponse.json(), resultat_attendu)