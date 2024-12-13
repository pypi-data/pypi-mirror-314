import datetime as dt
import decimal
import json
import os
from pprint import pprint

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from enedis.connection.enedis_connection import EnedisConnection
from enedis.services.commande_M023 import M023HistoriqueMesuresFines, M023MesuresFacturantes, \
    M023InformationsTechniquesEtContractuelles
from enedis.services.commande_acces_donnees_mesures import CommandeAccesDonneesMesures
from enedis.services.commander_arret_service_souscrit_mesures import CommanderArretServiceSouscritMesures
from enedis.services.commander_collecte_publication_mesures import CommanderCollectePublicationMesures
from enedis.services.consulter_donnees_techniques_contractuelles import ConsulterDoneesTechniquesContractuelles
from enedis.services.consulter_mesures import ConsulterMesures
from enedis.services.consulter_mesures_detaillees import ConsulterMesuresDetaillees
from enedis.services.consulter_point import ConsulterPoint
from enedis.services.rechercher_point import RecherchePoint
from enedis.services.recherche_services_souscrits_mesures import RechercheServicesSouscritsMesures


def deserializator(o):
    encoder = json.JSONEncoder()
    if isinstance(o, dt.time) or isinstance(o, dt.datetime) or isinstance(o, dt.date):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return float(o)
    else:
        return encoder.default(o)

class EnedisApiView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        enedis_url = os.environ['WS_ENEDIS_URL']
        login = os.environ['WS_ENEDIS_LOGIN']
        contrat_id = os.environ['WS_ENEDIS_CONTRAT_ID']
        self.connection = EnedisConnection(enedis_url, login, contrat_id)

class RecherchePointV2View(EnedisApiView):
    throttle_scope = 'rechercherpointv2'

    def post(self, request, format=None):
        msg, resultat = RecherchePoint.recherche_point(self.connection, request.data['donnees'])
        return Response(resultat)


class RechercherServicesSouscritsMesuresV1View(EnedisApiView):
    throttle_scope = 'rechercherservicessouscritsmesuresv1'

    def post(self, request, format=None):

        pprint(request.data['donnees'])
        msg, resultat = RechercheServicesSouscritsMesures.rechercher_services_souscrit_mesures(self.connection,
            request.data['donnees'])

        return Response(resultat)


class ConsultationPointV4View(EnedisApiView):
    throttle_scope = 'consultationpointv4'

    def post(self, request, format=None):
        msg, resultat = ConsulterPoint.consulter_donnees_point(self.connection, request.data['donnees'])
        return Response(resultat)


class ConsultationMesuresDetailleesV3View(EnedisApiView):
    throttle_scope = 'consultationmesuresdetailleesv3'

    def post(self, request, format=None):
        msg, resultat = ConsulterMesuresDetaillees.consulter_mesures_detaillees(self.connection, request.data['donnees'])
        return Response(resultat)


class ConsultationMesuresV1View(EnedisApiView):
    throttle_scope = 'consultationmesuresv1'

    def post(self, request, format=None):
        msg, resultat = ConsulterMesures.consulter_mesures(self.connection, request.data['donnees'])
        return Response(resultat)


class ConsultationDonneesTechniquesContractuellesV1View(EnedisApiView):
    throttle_scope = 'consultationdonneestechniquescontractuellesv1'

    def post(self, request, format=None):
        msg, resultat = ConsulterDoneesTechniquesContractuelles.consultation_donnees_techniques_contractuelles(
            self.connection, request.data['donnees'])
        return HttpResponse(json.dumps(resultat, default=deserializator).encode(), content_type='application/json')


class CommandeCollectePublicationMesuresV3View(EnedisApiView):
    throttle_scope = 'commandecollectepublicationmesuresv3'

    def post(self, request, format=None):
        msg, resultat = CommanderCollectePublicationMesures.commander_collecte_publication(self.connection, request.data['donnees'])
        return Response(resultat)


class CommandeArretServicesSouscritsMesuresV1View(EnedisApiView):
    throttle_scope = 'commandearretservicessouscritsmesuresv1'

    def post(self, request, format=None):
        msg, resultat = CommanderArretServiceSouscritMesures.commander_arret_service_souscrit_mesures(
            self.connection, request.data['donnees'])
        return Response(resultat)


class CommandeAccesDonneesMesuresV1View(EnedisApiView):
    throttle_scope = 'commandeaccesservicessouscritsv1'

    def post(self, request, format=None):
        msg, resultat = CommandeAccesDonneesMesures.commande_acces_donnees_mesures(self.connection, request.data['donnees'])
        return Response(resultat)

class CommandeHistoriqueDonneesMesuresFinesV1View(EnedisApiView):
    throttle_scope = 'commandem023historiquedonneesmesuresfinesv1'

    def post(self, request, format=None):
        msg, resultat = M023HistoriqueMesuresFines.m023(self.connection, request.data['donnees'])
        return Response(resultat)

class CommandeInformationsTechniquesEtContractuellesV1View(EnedisApiView):
    throttle_scope = 'commandem023informationstechniquesetcontractuellesv1'

    def post(self, request, format=None):
        msg, resultat = M023InformationsTechniquesEtContractuelles.m023(self.connection, request.data['donnees'])
        return Response(resultat)

class CommandeMesuresFacturantesV1View(EnedisApiView):
    throttle_scope = 'commandem023mesuresfacturantesv1'

    def post(self, request, format=None):
        msg, resultat = M023MesuresFacturantes.m023(self.connection, request.data['donnees'])
        return Response(resultat)
