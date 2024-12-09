from django.test import TestCase
from rest_framework.test import APIClient

from enedis.data_models.consultermesures import DonneesConsulterMesures
from proxy.models import TraceActivite


class TestTrace(TestCase):

    def test_log_base(self):
        client = APIClient()
        mauvaise_datas = {'serveur': 'pas le dernier', 'donnees': DonneesConsulterMesures('12345678911234', True)}
        client.post('/v1.1/consultermesures/', mauvaise_datas, format='json')
        client.post('/v1.1/consultermesures/', mauvaise_datas, format='json')
        client.post('/v1.1/consultermesures/', mauvaise_datas, format='json')
        client.post('/v1.1/consultermesures/', mauvaise_datas, format='json')

        datas = {'serveur': 'poste_test_base_de_donnees', 'donnees': DonneesConsulterMesures('95376291856439', True)}
        client.post('/v1.1/consultermesures/', datas, format='json')
        derniere_entree = TraceActivite.objects.latest('horodate')
        self.assertEqual(derniere_entree.RAE_concerne, datas['donnees']['pointId'])
        self.assertEqual(derniere_entree.demandeur, datas['serveur'])
