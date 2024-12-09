from utils.regex import verification_prm


class ConsulterDonneesTechniquesContractuelles(dict):
    def __init__(self, point_id: str, autorisation_client=False):
        verification_prm(point_id)
        dict.__init__(self, pointId=point_id, autorisationClient=autorisation_client, loginUtilisateur='')
