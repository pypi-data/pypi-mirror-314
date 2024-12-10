from django.test import RequestFactory, TestCase

from djangocms_export_page.export.common import PageExport
from djangocms_export_page.export.docx import DocxPageExport

from .factories import BlogFactory


class ExportModelTests(TestCase):
    def setUp(self):
        self.object = BlogFactory()
        self.language = "nl"
        self.request = RequestFactory().get(self.object.get_absolute_url())

    def test_model_export(self):
        export = DocxPageExport(self.request, self.object, language=self.language)
        export_file = export.export()
        self.assertEqual(type(export_file), bytes)

    def test_page_url(self):
        export = PageExport(self.request, self.object, language=self.language)
        self.assertEqual(
            export.page_url, "http://example.com" + self.object.get_absolute_url()
        )
