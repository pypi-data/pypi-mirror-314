from functools import wraps
from http.client import RemoteDisconnected

import zeep

from utils.soap import logger


def universal_error_handling(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            retour = func(*args, **kwargs)
        except (TypeError, zeep.exceptions.TransportError, zeep.exceptions.Fault, zeep.exceptions.ValidationError,
                ValueError, RemoteDisconnected) as erreur:
            retour = {'erreur': str(erreur.args), 'status': 'failed'}
            logger.exception(
                f'le service {func.__name__} n\'a pas mené à bien sa mission : code {retour["status"]}. detail de l\'erreur : \n {retour["erreur"]}')

        return retour

    return inner
