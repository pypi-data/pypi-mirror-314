import os
import unittest

import zeep
from django.test import TestCase

from enedis.connection.enedis_connection import EnedisConnection


class ServicesTestCase(TestCase):

    def setUp(self):
        enedis_url = os.getenv('WS_ENEDIS_URL', "http://imposter:8080/")
        self.connection = EnedisConnection(enedis_url, 'test@test.fr', '1111111')


def raise_transport_errror(*args, **kwargs):
    raise zeep.exceptions.TransportError("une erreur inconnue est survenue")


def raise_creation_error(*args, **kwargs):
    raise ValueError('test pour voir si cela fonctionne')
