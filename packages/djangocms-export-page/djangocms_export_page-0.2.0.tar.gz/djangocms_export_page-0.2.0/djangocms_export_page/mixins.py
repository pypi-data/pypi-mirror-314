from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .constants import FILE_FORMATS


class ExportPageMixin:

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # This might be silly to call it there, but at least it’s late enough
    #     self.create_menu()
    #     return context

    # def create_menu(self):
    #     """
    #     Create a menu for your Model. Example code:

    #     menu = self.request.toolbar.get_or_create_menu(
    #         self.get_context_object_name(self.object),
    #         self.toolbar_menu_label
    #     )

    #     change_url = reverse_lazy(
    #         'admin:{m.app_label}_{m.model_name}_change'.format(m=self.model._meta),
    #         args=[self.object.id]
    #     )
    #     menu.add_sideframe_item(self.toolbar_change_label, url=change_url)

    #     self.create_export_page_menu_entry(menu)
    #     """

    #     try:
    #         super().create_menu()
    #     except AttributeError:
    #         raise NotImplementedError

    def create_export_page_menu_entry(self, current_page_menu):
        current_page_menu.add_break("export-page-break")
        file_formats = FILE_FORMATS.values()

        if len(file_formats) == 1:
            menu = current_page_menu
        else:
            menu = current_page_menu.get_or_create_menu("export-page", _("Export"))

        for file_format in file_formats:
            label = _("Export to {ext}").format(ext="." + file_format.ext)
            export_url = reverse(
                "export-page:model",
                kwargs={
                    "app": self.object._meta.app_label,
                    "model": self.object._meta.model_name,
                    "pk": self.object.pk,
                    "file_format": file_format.name,
                },
            )
            menu.add_link_item(label, url=export_url)
