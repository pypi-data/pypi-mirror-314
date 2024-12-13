import datetime as dt
from time import sleep

import pandas as pd

from enedis.services.commande_M023 import M023Base
from enedis.services.commande_acces_donnees_mesures import CommandeAccesDonneesMesures
from enedis.services.commander_arret_service_souscrit_mesures import CommanderArretServiceSouscritMesures
from enedis.services.commander_collecte_publication_mesures import CommanderCollectePublicationMesures
from enedis.services.consulter_donnees_techniques_contractuelles import ConsulterDoneesTechniquesContractuelles  # OK
from enedis.services.consulter_mesures import ConsulterMesures  # OK
from enedis.services.consulter_mesures_detaillees import ConsulterMesuresDetaillees  # OK
from enedis.services.recherche_services_souscrits_mesures import RechercheServicesSouscritsMesures
from enedis.services.rechercher_point import RecherchePoint  # OK
from enedis.data_models.M023 import DemandeHistoriqueMesuresFines, \
    DemandeHistoriqueDonneesFacturantes, DemandeInformationsTechniquesEtContractuelles
from enedis.data_models.commandeaccesdonneesmesures import Contrat, \
    DemandeAccesDonneesMesures, AccesDonnees, DonneesGeneralesAccesDonnees
from enedis.data_models.commanderarretservicesouscritmesures import \
    DemandeArretServiceSouscritMesures, ArretServiceSouscrit, DonneesGeneralesArretService
from enedis.data_models.commandercollectepublicationmesures import DemandeCollectePublicationMesure, \
    AccesMesures, DonneesGeneralesDemandeCollecte
from enedis.data_models.common import DeclarationAccordClient, PersonnePhysique
from enedis.data_models.consulterdonneestechniquescontractuelles import Point  # OK
from enedis.data_models.consultermesures import DonneesConsulterMesures  # OK
from enedis.data_models.consultermesuresdetaillees import \
    DemandeConsulterMesuresDetaillees  # OK
from enedis.data_models.recherchepoint import AdresseInstallation, Criteres  # OK

LIST_C2C4 = ['98800004935121', '98800001544168', '98800004938924', '98800006694381', '98800001220186']
LIST_C5 = ['25150217034354', '25825036170379', '25999131613803', '50086054270348', '25262662681289']

CAS_TEST = [{'function': ConsulterDoneesTechniquesContractuelles.consultation_donnees_techniques_contractuelles,
             'params': [Point(point_id='98800007059999', autorisation_client=True),
                        Point(point_id='25946599093143', autorisation_client=True),
                        Point(point_id='98800007059999', autorisation_client=False),
                        Point(point_id='25946599093143', autorisation_client=False),
                        Point(point_id='99999999999999')]
             },
            {'function': ConsulterMesures.consulter_mesures,
             'params': [DonneesConsulterMesures(point_id='30001610071843', autorisation_client=True),
                        DonneesConsulterMesures(point_id='25957452924301', autorisation_client=True),
                        DonneesConsulterMesures(point_id='30001610071843', autorisation_client=False),
                        ]
             },
            {'function': ConsulterMesuresDetaillees.consulter_mesures_detaillees,
             'params': [DemandeConsulterMesuresDetaillees('30001610071843', TypeDonneesM023.CDC, GrandeurPhysique.PA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),
                        DemandeConsulterMesuresDetaillees('25478147557460', TypeDonneesM023.CDC, GrandeurPhysique.PA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('30001610071843', TypeDonneesM023.CDC,
                                                          GrandeurPhysique.PRI,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('30001610071843',
                                                          TypeDonneesM023.ENERGIE,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('25478147557460',
                                                          TypeDonneesM023.ENERGIE,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('25478147557460',
                                                          TypeDonneesM023.PMAX,
                                                          GrandeurPhysique.PMA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT, mesures_pas=MesuresPas.JOUR),

                        DemandeConsulterMesuresDetaillees('30001610071843',
                                                          TypeDonneesM023.INDEX,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('25478147557460',
                                                          TypeDonneesM023.INDEX,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('30001610071843',
                                                          TypeDonneesM023.INDEX,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.SERVICE_ACCES),

                        DemandeConsulterMesuresDetaillees('25478147557460',
                                                          TypeDonneesM023.INDEX,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 7)
                                                          , False, CadreAcces.SERVICE_ACCES),

                        DemandeConsulterMesuresDetaillees('25478147557460',
                                                          TypeDonneesM023.CDC,
                                                          GrandeurPhysique.PA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 9)
                                                          , False, CadreAcces.ACCORD_CLIENT),

                        DemandeConsulterMesuresDetaillees('25478147557460',
                                                          TypeDonneesM023.INDEX,
                                                          GrandeurPhysique.EA,
                                                          SensMesure.SOUTIRAGE, dt.date(2022, 4, 1), dt.date(2022, 4, 8)
                                                          , False, CadreAcces.SERVICE_ACCES)
                        ]
             },
            {'function': RecherchePoint.recherche_point,
             'params': [
                 Criteres(adresse_installation=AdresseInstallation(code_postal='34650', code_insee_commune='34231'),
                          domaine_tension_alimentation_code=DomaineTension.BTINF,
                          categorie_client_final_code=ClientFinalCategorieCode.RES),

                 Criteres(adresse_installation=AdresseInstallation(code_postal='84160', code_insee_commune='84042',
                                                                   numero_et_nom_voie='1 RUE DE LA MER'),
                          nom_client_final_ou_denomination_sociale='TEST', recherche_hors_perimetre=True),

                 Criteres(adresse_installation=AdresseInstallation(code_postal='84160', code_insee_commune='84042',
                                                                   numero_et_nom_voie='1 RUE DE LA MER'),
                          nom_client_final_ou_denomination_sociale='TES', recherche_hors_perimetre=True),

                 Criteres(adresse_installation=AdresseInstallation(code_postal='34650', code_insee_commune='34231'),
                          categorie_client_final_code=ClientFinalCategorieCode.RES),

                 Criteres(adresse_installation=AdresseInstallation(code_insee_commune='34231',
                                                                   numero_et_nom_voie='404 rue de la demande invalide'))

             ]
             },
            {'function': CommandeAccesDonneesMesures.commande_acces_donnees_mesures,
             'params': [DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('24380318190106', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.ENERGIE, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('98800002267746', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.ENERGIE, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('24380318190106', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.CDC, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('98800002267746', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.CDC, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('24380318190106', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.PMAX, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('24380318190106', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.INDEX, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('98800002267746', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.INDEX, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('24380318190106', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.ENERGIE, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=False))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('98800002267746', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2025, 1, 1),
                                                                TypeDonneesV1.ENERGIE, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=False))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('24380318190106', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2077, 1, 1),
                                                                TypeDonneesV1.ENERGIE, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True))),

                        DemandeAccesDonneesMesures(DonneesGeneralesAccesDonnees('98800002267746', Contrat()),
                                                   AccesDonnees(dt.date.today(), dt.date(2077, 1, 1),
                                                                TypeDonneesV1.ENERGIE, TypeSite.INJECTION,
                                                                DeclarationAccordClient(PersonnePhysique('Michu'), accord=True)))
                        ]
             },
            {'function': CommanderCollectePublicationMesures.commander_collecte_publication,
             'params': [
                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('25884515170669'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(
                                                  PersonnePhysique('Michu'),
                                                  accord=True),
                                              TypeDonneesV1.CDC,
                                              True,
                                              False,
                                              PasMesures.P30MIN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE)),
                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('98800000000246'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=True),
                                              TypeDonneesV1.CDC, True, False,
                                              PasMesures.P10MIN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('25884515170669'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=True),
                                              TypeDonneesV1.CDC, True, False,
                                              PasMesures.P30MIN,
                                              transmission_recurrente=False,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('98800000000246'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=True),
                                              TypeDonneesV1.CDC, True, False,
                                              PasMesures.P10MIN,
                                              transmission_recurrente=False,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('25884515170669'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=True),
                                              TypeDonneesV1.INDEX, True, False,
                                              PasMesures.QUOTIDIEN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('98800000000246'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=True),
                                              TypeDonneesV1.INDEX, True, False,
                                              PasMesures.QUOTIDIEN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('25884515170669'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=4*365),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=True),
                                              TypeDonneesV1.CDC, True, False,
                                              PasMesures.P30MIN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('25884515170669'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=False),
                                              TypeDonneesV1.CDC, True, False,
                                              PasMesures.P30MIN,
                                              transmission_recurrente=False,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('98800000000246'),
                                                  AccesMesures(dt.date.today() + dt.timedelta(days=10), dt.date.today() +
                                              dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=False),
                                              TypeDonneesV1.CDC, True, False,
                                              PasMesures.P10MIN,
                                              transmission_recurrente=False,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('25884515170669'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=False),
                                              TypeDonneesV1.INDEX, True, False,
                                              PasMesures.QUOTIDIEN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE,
                                              mesures_corrigees=False)),

                 DemandeCollectePublicationMesure(DonneesGeneralesDemandeCollecte('98800000000246'),
                                                  AccesMesures(dt.date.today(), dt.date.today() + dt.timedelta(days=200),
                                              DeclarationAccordClient(PersonnePhysique('Michu'), accord=False),
                                              TypeDonneesV1.INDEX, True, False,
                                              PasMesures.QUOTIDIEN,
                                              transmission_recurrente=True,
                                              periodicite_transmission=PeriodiciteTransmission.QUOTIDIENNE,
                                              mesures_corrigees=False))

             ]},
            {'function': RechercheServicesSouscritsMesures.rechercher_services_souscrit_mesures,
             'params': ['25884515170669',
                        '98800000000246']
             },
            {'function': CommanderArretServiceSouscritMesures.commander_arret_service_souscrit_mesures,
             'params': [DemandeArretServiceSouscritMesures(DonneesGeneralesArretService('25884515170669'), ArretServiceSouscrit('12')),
                        DemandeArretServiceSouscritMesures(DonneesGeneralesArretService('98800000000246'), ArretServiceSouscrit('12'))]
             },

            {'function': M023Base.m023,
             'params': [DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.ENERGIE, LIST_C5,
                                                      FormatsM023.JSON, False),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.ENERGIE, LIST_C2C4,
                                                      FormatsM023.CSV, True),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.CDC, ['25150217034354'],
                                                      FormatsM023.CSV, False),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.CDC, ['98800004935121'],
                                                      FormatsM023.CSV, True),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.PMAX, ['25150217034354'],
                                                      FormatsM023.CSV, False),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.PMAX, ['98800004935121'],
                                                      FormatsM023.CSV, True),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.INDEX, LIST_C5,
                                                      FormatsM023.JSON, False),
                        DemandeHistoriqueMesuresFines(dt.date(2023, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.INDEX, LIST_C2C4,
                                                      FormatsM023.CSV, True),
                        DemandeHistoriqueMesuresFines(dt.date(2020, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.CDC, LIST_C5,
                                                      FormatsM023.CSV, False),
                        DemandeHistoriqueMesuresFines(dt.date(2020, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.CDC, LIST_C2C4,
                                                      FormatsM023.CSV, True),
                        DemandeHistoriqueMesuresFines(dt.date(2019, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.INDEX, LIST_C5,
                                                      FormatsM023.CSV, False),
                        DemandeHistoriqueMesuresFines(dt.date(2019, 1, 1),
                                                      dt.date(2023, 6, 1),
                                                      CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                      TypeDonneesM023.INDEX, LIST_C2C4,
                                                      FormatsM023.CSV, True),

                        DemandeHistoriqueDonneesFacturantes(dt.date(2023, 1, 1),
                                                            dt.date(2023, 6, 1),
                                                            CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                            LIST_C5,
                                                            FormatsM023.CSV),
                        DemandeHistoriqueDonneesFacturantes(dt.date(2023, 1, 1),
                                                            dt.date(2023, 6, 1),
                                                            CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                            LIST_C2C4,
                                                            FormatsM023.CSV),

                        DemandeHistoriqueDonneesFacturantes(dt.date(2023, 6, 1),
                                                            dt.date(2023, 1, 1),
                                                            CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                            LIST_C5,
                                                            FormatsM023.CSV),
                        DemandeHistoriqueDonneesFacturantes(dt.date(2023, 6, 1),
                                                            dt.date(2023, 1, 1),
                                                            CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                            LIST_C2C4,
                                                            FormatsM023.CSV),

                        DemandeInformationsTechniquesEtContractuelles(CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                                      LIST_C5,
                                                                      FormatsM023.CSV),
                        DemandeInformationsTechniquesEtContractuelles(CadreAcces.ACCORD_CLIENT, SensMesure.SOUTIRAGE,
                                                                      LIST_C2C4,
                                                                      FormatsM023.CSV),
                        ]
             },
            ]


def run():
    results = dict(nom_service=[], date_appel=[], date_reception=[], dict_params=[], message_recu=[])
    for test in CAS_TEST:
        for param in test['params']:
            date_envoi = dt.datetime.now()
            f = test['function'](param)
            date_reception = dt.datetime.now()
            results['nom_service'].append(test['function'].__name__)
            results['date_appel'].append(date_envoi)
            results['date_reception'].append(date_reception)
            results['dict_params'].append(param)
            results['message_recu'].append(f)
            sleep(1)
    results_df = pd.DataFrame(results)
    results_df.to_csv('resultats_homologation.csv')
