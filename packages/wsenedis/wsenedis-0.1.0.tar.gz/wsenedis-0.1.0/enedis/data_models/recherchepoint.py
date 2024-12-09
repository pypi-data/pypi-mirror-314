from .const import DomaineTension, ClientFinalCategorieCode


class AdresseInstallation(dict):
    def __init__(self, escalier_etage_et_appartement: str = None, batiment: str = None, numero_et_nom_voie: str = None,
                 lieu_dit: str = None, code_postal: str = None, code_insee_commune: str = None):
        _kwargs = {}
        if escalier_etage_et_appartement is not None:
            _kwargs['escalierEtEtageEtAppartement'] = escalier_etage_et_appartement
        if batiment is not None:
            _kwargs['batiment'] = batiment
        if numero_et_nom_voie is not None:
            _kwargs['numeroEtNomVoie'] = numero_et_nom_voie
        if lieu_dit is not None:
            _kwargs['lieuDit'] = lieu_dit
        if code_postal is not None:
            _kwargs['codePostal'] = code_postal
        if code_insee_commune is not None:
            _kwargs['codeInseeCommune'] = code_insee_commune
        dict.__init__(self, **_kwargs)


class Criteres(dict):
    def __init__(self, num_siret: str = None, matricule_ou_numero_serie: str = None,
                 domaine_tension_alimentation_code: DomaineTension = None,
                 nom_client_final_ou_denomination_sociale: str = None,
                 categorie_client_final_code: ClientFinalCategorieCode = None, recherche_hors_perimetre: bool = None,
                 adresse_installation: AdresseInstallation = None):
        _kwargs = {}
        if num_siret is not None:
            _kwargs['numSiret'] = num_siret
        if matricule_ou_numero_serie is not None:
            _kwargs['matriculeOuNumeroSerie'] = matricule_ou_numero_serie
        if domaine_tension_alimentation_code is not None:
            _kwargs['domaineTensionAlimentationCode'] = domaine_tension_alimentation_code.value
        if nom_client_final_ou_denomination_sociale is not None:
            _kwargs['nomClientFinalOuDenominationSociale'] = nom_client_final_ou_denomination_sociale
        if categorie_client_final_code is not None:
            _kwargs['categorieClientFinalCode'] = categorie_client_final_code.value
        if recherche_hors_perimetre is not None:
            _kwargs['rechercheHorsPerimetre'] = recherche_hors_perimetre
        if adresse_installation is not None:
            _kwargs['adresseInstallation'] = adresse_installation
        dict.__init__(self, **_kwargs)

class RechercherPoint(dict):
    def __init__(self, criteres: Criteres):
        dict.__init__(self, criteres=criteres, loginUtilisateur='')