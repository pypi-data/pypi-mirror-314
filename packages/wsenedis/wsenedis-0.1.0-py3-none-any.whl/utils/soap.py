import os
import re
from django.conf import settings as django_settings
from lxml import etree
from zeep import Settings, Client, Plugin

from enedis.connection.enedis_connection import EnedisConnection
from enedis.utils.wsdl import wsdl
import logging

logger = logging.getLogger(__name__)



def soap_service(name: str, ns: str, port_binding: str, service_path: str, tn_binding=None):
    settings = Settings(strict=True, xml_huge_tree=True)
    # Récupération du singleton connexion
    connexion = EnedisConnection()
    client = Client(wsdl=wsdl(name), transport=connexion.get_transport(), settings=settings,
                            plugins=[FixMalformedDatesPlugin()])

    url = django_settings.WS_ENEDIS_URL
    login = django_settings.WS_ENEDIS_LOGIN

    service_proxy = client.create_service(f'{{{tn_binding}}}{port_binding}', os.path.join(url, service_path))
    factory = client.type_factory(ns)

    return service_proxy, factory, login, client

# def handler_soap_response(func):
#     def inner(*args, **kwargs):
#         response = func(*args, **kwargs)
#         # if 'erreur' in response:
#         #     logger.warning(
#         #         f'Service request {func.__name__} has failed : code {response["status"]}. Content : \n {response["erreur"]}')
#
#         return response
#     return inner

