from __future__ import annotations

import datetime as dt

from enedis.utils.regex import verification_prm
from .common import DeclarationAccordClient
from .const import TypeDonneesV1, PeriodiciteTransmission, PasMesures


class AccesMesures(dict):
    def __init__(self, date_debut: dt.date, date_fin: dt.date, declaration_accord_client: DeclarationAccordClient,
                 mesure_type: TypeDonneesV1, soutirage: bool, injection: bool, mesures_pas: PasMesures,
                 transmission_recurrente: bool, periodicite_transmission: PeriodiciteTransmission = None,
                 mesures_corrigees: bool = None):
        _kwargs = {'dateDebut': date_debut, 'dateFin': date_fin, 'declarationAccordClient': declaration_accord_client,
                   'mesuresTypeCode': mesure_type.value, 'soutirage': soutirage, 'injection': injection,
                   'mesuresPas': mesures_pas.value,
                   'transmissionRecurrente': transmission_recurrente}
        if mesures_corrigees is not None:
            _kwargs['mesuresCorrigees'] = mesures_corrigees
        if periodicite_transmission is not None:
            _kwargs['periodiciteTransmission'] = periodicite_transmission.value

        dict.__init__(self, **_kwargs)


class DonneesGeneralesDemandeCollecte(dict):
    def __init__(self, point_id: str, objet_code='AME', ref_externe=None):
        verification_prm(point_id)
        _kwargs = {'pointId': point_id, 'objetCode': objet_code, 'initiateurLogin': '', 'contratId': ''}
        if ref_externe is not None:
            _kwargs['refExterne'] = ref_externe
        dict.__init__(self, **_kwargs)


class DemandeCollectePublicationMesure(dict):
    def __init__(self, donnees_generales: DonneesGeneralesDemandeCollecte, acces_mesures: AccesMesures):
        dict.__init__(self, donneesGenerales=donnees_generales, accesMesures=acces_mesures)
