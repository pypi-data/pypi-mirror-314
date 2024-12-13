from enedis.services.rechercher_point import RecherchePoint
import datetime as dt


def run():
    print(f'message envoyé à {dt.datetime.now()}')

    reponse = RecherchePoint.recherche_point(Criteres('12345678911234'))

    print(f'message reçu à {dt.datetime.now()}: \n {reponse}')
