from __future__ import annotations

import datetime as dt

from .common import DeclarationAccordClient
from .const import TypeDonneesV1, TypeSite


class Contrat(dict):

    def __init__(self, acteur_marche_code=None, contrat_type=None):
        _kwargs = {'contratId': ""}
        if acteur_marche_code is not None:
            _kwargs["acteurMarcheCode"] = acteur_marche_code
        if contrat_type is not None:
            _kwargs['contratType'] = contrat_type
        dict.__init__(self, **_kwargs)


class AccesDonnees(dict):

    def __init__(self, date_debut: dt.date, date_fin: dt.date, type_donnees: TypeDonneesV1, type_site: TypeSite,
                 declaration_accord_client: DeclarationAccordClient):
        _kwargs = {'dateDebut': date_debut, 'dateFin': date_fin, 'typeDonnees': type_donnees.value,
                   'declarationAccordClient': declaration_accord_client}
        if type_site == TypeSite.SOUTIRAGE:
            _kwargs['soutirage'] = True
        if type_site == TypeSite.INJECTION:
            _kwargs['injection'] = True
        dict.__init__(self, **_kwargs)


class DonneesGeneralesAccesDonnees(dict):
    def __init__(self, point_id: str, contrat: Contrat, ref_externe=None):
        _kwargs = {'objetCode': "AME", 'pointId': point_id, 'initiateurLogin': "", 'contrat': contrat}
        if ref_externe is not None:
            _kwargs['refExterne'] = ref_externe
        dict.__init__(self, **_kwargs)


class DemandeAccesDonneesMesures(dict):

    def __init__(self, donnees_generales: DonneesGeneralesAccesDonnees, acces_donnees: AccesDonnees):
        _kwargs = {'donneesGenerales': donnees_generales, 'accesDonnees': acces_donnees}
        dict.__init__(self, **_kwargs)
