from django.test import TestCase

from djangocms_export_page.utils import clean_value


class CleanValueTests(TestCase):

    def test_clean_value_noop(self):
        value = "Vrĳ België"
        self.assertEqual(clean_value(value), value)

    def test_clean_value_n(self):
        value = "Vrĳ\nBelgië"
        self.assertEqual(clean_value(value), value)

    def test_clean_value_rn(self):
        value = "Vrĳ\r\nBelgië"
        self.assertEqual(clean_value(value), value)

    def test_clean_value_f(self):
        self.assertEqual(clean_value("Vrĳ\f België"), "Vrĳ België")

    def test_clean_value_stripped(self):
        self.assertEqual(clean_value("\r\n Vrĳ België\n "), "Vrĳ België")
