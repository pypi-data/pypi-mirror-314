from __future__ import annotations

import datetime as dt
import os

from utils.regex import verification_prm
from .const import CadreAcces, SensMesure, FormatsM023, TypeDonneesM023

MAX_PRMS = 1500

class DemandeM023(dict):
    def __init__(self, *args, **kwargs):
        _kwargs = {"donneesGenerales": {"initiateurLogin": "", "contratId": ""}, "demande": {}}
        dict.__init__(self, **_kwargs)

    def check_dates(self):
        if not bool(os.getenv('HOMOLOGATION', False)):
            if ((self['demande'] is not None) and ("dateDebut" in self['demande'])
                    and (self['demande']['dateDebut'] > self['demande']['dateFin'])):
                raise ValueError(
                    'incohérence temporelle au niveau des dates. la date de fin est supérieure à la date du jour ou '
                    'antérieure à la date de début')


class DemandeHistoriqueMesuresFines(DemandeM023):
    def __init__(self,
                 date_debut: dt.date,
                 date_fin: dt.date,
                 cadre_acces: CadreAcces,
                 sens: SensMesure,
                 mesure_type_code: TypeDonneesM023,
                 points: [str],
                 format: FormatsM023,
                 mesures_corrigees: bool = None):
        super().__init__()

        if len(points) == 0:
            raise ValueError('il faut renseigner au moins un PRM')
        elif len(points) > MAX_PRMS:
            raise ValueError('Trop de prms demandés')
        else:
            _kwargs = {"pointIds": [], "mesuresTypeCode": mesure_type_code.value, "sens": sens.value,
                       "cadreAcces": cadre_acces.value,
                       "dateDebut": date_debut, "dateFin": date_fin, "format": format.value}
            for point in points:
                verification_prm(point)
                _kwargs['pointIds'].append({'pointId': point})
            if mesures_corrigees is not None:
                _kwargs['mesuresCorrigees'] = mesures_corrigees
            self['demande'] = _kwargs
        self.check_dates()


class DemandeHistoriqueDonneesFacturantes(DemandeM023):
    def __init__(self, date_debut: dt.date, date_fin: dt.date, cadre_acces: CadreAcces, sens: SensMesure,
                 points: [str], format: FormatsM023):
        super().__init__()
        if len(points) == 0:
            raise ValueError('il faut renseigner au moins un PRM')
        elif len(points) > MAX_PRMS:
            raise ValueError('Trop de prms demandés')
        else:
            _kwargs = {"pointIds": [], "sens": sens.value, "cadreAcces": cadre_acces.value, "dateDebut": date_debut,
                       "dateFin": date_fin, "format": format.value}
            for point in points:
                verification_prm(point)
                _kwargs['pointIds'].append({'pointId': point})
            self['demande'] = _kwargs
        self.check_dates()


class DemandeInformationsTechniquesEtContractuelles(DemandeM023):
    def __init__(self, cadre_acces: CadreAcces, sens: SensMesure, points: [str], format: FormatsM023) -> object:
        super().__init__()
        if len(points) == 0:
            raise ValueError('il faut renseigner au moins un PRM')
        elif len(points) > MAX_PRMS:
            raise ValueError('Trop de prms demandés')
        else:
            _kwargs = {"pointIds": [], "sens": sens.value, "cadreAcces": cadre_acces.value, "format": format.value}
            for point in points:
                verification_prm(point)
                _kwargs['pointIds'].append({'pointId': point})
            self['demande'] = _kwargs

