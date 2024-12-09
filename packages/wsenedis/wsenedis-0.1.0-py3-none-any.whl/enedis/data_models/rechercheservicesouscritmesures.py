from utils.regex import verification_prm


class Criteres(dict):
    def __init__(self, point_id):
        verification_prm(point_id)
        dict.__init__(self, contratId='', pointId=point_id)

class RechercherServicesSouscritsMesures(dict):
    def __init__(self, criteres: Criteres):
        dict.__init__(self, criteres=criteres, loginUtilisateur='')
