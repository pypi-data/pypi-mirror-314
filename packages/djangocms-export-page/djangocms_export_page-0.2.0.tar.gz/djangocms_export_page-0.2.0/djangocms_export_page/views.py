from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import get_language
from django.views.generic import View

from cms.models import Page

from .constants import FILE_FORMATS, PAGE_EXPORTS


class PageExportView(UserPassesTestMixin, View):
    response_class = HttpResponse
    export_classes = PAGE_EXPORTS

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(*args, **kwargs)
        self.language = get_language()
        self.file_format = FILE_FORMATS[kwargs.pop("file_format")]
        return self.render_to_response(request)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Page, pk=kwargs.pop("page_pk"))

    def render_to_response(self, request):
        export_class = self.export_classes[self.file_format.name]
        export_file = export_class(
            request, self.object, language=self.language
        ).export()
        content_type = self.file_format.content_type

        response = self.response_class(export_file, content_type=content_type)
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(
            self.get_file_name()
        )
        return response

    def get_file_name(self):
        title = self.object.get_title(language=self.language)

        return "{name}_{lang}.{ext}".format(
            name=slugify(title),
            lang=self.language,
            ext=self.file_format.ext,
        )


class ModelExportView(PageExportView):

    def get_object(self, *args, **kwargs):
        app_name, model, pk = [kwargs.pop(arg) for arg in ("app", "model", "pk")]
        content_type = ContentType.objects.get_by_natural_key(app_name, model)
        return content_type.get_object_for_this_type(pk=pk)
