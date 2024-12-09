from utils.regex import verification_prm
from .const import GrandeurPhysique, SensMesure, MesuresPas, CadreAcces, TypeDonnees
import datetime as dt


class DemandeConsulterMesuresDetaillees(dict):
    def __init__(self, point_id: str, mesures_type_code: TypeDonnees, grandeur_physique: GrandeurPhysique,
                 sens: SensMesure,
                 date_debut: dt.date, date_fin: dt.date, mesures_corrigees: bool, cadre_acces: CadreAcces,
                 mesures_pas: MesuresPas = None):
        verification_prm(point_id)
        _kwargs = {
            'initiateurLogin': '',
            'pointId': point_id,
            'mesuresTypeCode': mesures_type_code.value,
            'grandeurPhysique': grandeur_physique.value,
            'sens': sens.value,
            'dateDebut': date_debut,
            'dateFin': date_fin,
            'mesuresCorrigees': mesures_corrigees,
            'cadreAcces': cadre_acces.value
        }

        if mesures_pas is not None:
            _kwargs['mesuresPas'] = mesures_pas.value
        dict.__init__(self, **_kwargs)
