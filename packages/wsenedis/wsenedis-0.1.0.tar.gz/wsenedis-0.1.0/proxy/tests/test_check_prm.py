
from django.test import TestCase

from utils.regex import verification_prm


class TestCheckPrm(TestCase):

    def test_prm(self):
        prm = "01234567891234"
        verification_prm(prm)
        wrong_prm = "01"
        self.assertRaises(ValueError, verification_prm, wrong_prm)
