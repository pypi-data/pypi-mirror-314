import enum

FACTORY_DATA_SIMPLE = 'http://www.enedis.fr/sge/b2b/dictionnaire/v5.0/ds'


class PasCdc(enum.Enum):
    DIX_MINUTES = {'valeur': 10, 'unite': 'min'}
    TRENTE_MINUTES = {'valeur': 30, 'unite': 'min'}


class DomaineTension(enum.Enum):
    BTINF = 'BTINF'
    BTSUP = 'BTSUP'
    HTA = 'HTA'
    HTB = 'HTB'


class ClientFinalCategorieCode(enum.Enum):
    PRO = 'PRO'
    RES = 'RES'


class GrandeurPhysique(enum.Enum):
    PA = 'PA'
    PRI = 'PRI'
    PRC = 'PRC'
    E = 'E'
    TOUT = 'TOUT'
    PMA = 'PMA'
    EA = 'EA'


class MesuresPas(enum.Enum):
    JOUR = 'P1D'
    MOIS = 'P1M'


class GrandeursPhysiquesConsultationv3(enum.Enum):
    PUISSANCE_ACTIVE = 'PA'
    PUISSANCE_REACTIVE_INDUCTIVE = 'PRI'
    PUISSANCE_REACTIVE_CAPACITIVE = 'PRC'
    TENSION = 'E'
    TOUT = 'TOUT'
    PUISSANCES_MAX = 'PMA'
    ENERGIE_QUOTIDIENNE = 'EA'
    ENERGIE_ACTIVE = 'EA'
    ENERGIE_REACTIVE = 'ER'
    ENERGIE_REACTIVE_CAPACITIVE = 'ERC'
    ENERGIE_REACTIVE_INDUCTIVE = 'ERI'
    DUREE_DE_DEPASSEMENT = 'DD'
    DEPASSEMENT_ENERGETIQUE = 'DE'
    DEPASSEMENT_QUADRATIQUE = 'DQ'
    PUISSANCE_MAX_ATTEINTE = 'PMAX'
    TEMPS_DE_FONCTIONNEMENT = 'TF'


class PasMesures(enum.Enum):
    QUOTIDIEN = 'P1D'
    MENSUEL = 'P1M'
    P10MIN = 'PT10M'  # only for C1 C2 C3 C4 and P1 P2 P3
    P30MIN = 'PT30M'  # only for C5 and P4


class PeriodiciteTransmission(enum.Enum):
    QUOTIDIENNE = 'P1D'
    HEBDOMADAIRE = 'P7D'
    MENSUELLE = 'P1M'


class TypeDonneesV1(enum.Enum):
    CDC = 'CDC'
    INDEX = 'IDX'
    PMAX = 'PMAX'
    ENERGIE = 'ENERGIE'


class TypeDonnees(enum.Enum):
    CDC = 'COURBE'
    INDEX = 'INDEX'
    PMAX = 'PMAX'
    ENERGIE = 'ENERGIE'


class TypeDonneesM023(enum.Enum):
    CDC = 'COURBES'
    INDEX = 'INDEX'
    PMAX = 'PMAX'
    ENERGIE = 'ENERGIE'

class SensMesure(enum.Enum):
    INJECTION = 'INJECTION'
    SOUTIRAGE = 'SOUTIRAGE'


class CadreAcces(enum.Enum):
    ACCORD_CLIENT = "ACCORD_CLIENT"
    SERVICE_ACCES = "SERVICE_ACCES"
    EST_TITULAIRE = "EST_TITULAIRE"


class TypeSite(enum.Enum):
    SOUTIRAGE = "soutirage"
    INJECTION = "injection"


class FormatsM023(enum.Enum):
    JSON = "JSON"
    CSV = 'CSV'
