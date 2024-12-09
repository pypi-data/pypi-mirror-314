

class DonneesConsulterMesures(dict):
    def __init__(self, point_id: str, autorisation_client=False):
        _kwargs = {'pointId': point_id, 'loginDemandeur': '', 'contratId': '', 'autorisationClient': autorisation_client}
        dict.__init__(self, **_kwargs)
