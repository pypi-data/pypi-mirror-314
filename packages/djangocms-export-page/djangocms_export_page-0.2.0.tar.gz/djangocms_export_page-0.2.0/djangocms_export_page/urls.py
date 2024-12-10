from django.urls import re_path

from .views import ModelExportView, PageExportView

app_name = "export-page"

urlpatterns = [
    re_path(
        r"^(?P<page_pk>\d+)/(?P<file_format>\w+)/$",
        PageExportView.as_view(),
        name="cms_page",
    ),
    re_path(
        r"^(?P<app>\w+):(?P<model>\w+)/(?P<pk>\d+)/(?P<file_format>\w+)/$",
        ModelExportView.as_view(),
        name="model",
    ),
]
