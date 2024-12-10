from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.api import get_page_draft
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.page_permissions import user_can_change_page

from .constants import FILE_FORMATS


@toolbar_pool.register
class ExportPageToolbar(CMSToolbar):

    def populate(self):
        page = get_page_draft(self.request.current_page)

        if not page or not user_can_change_page(self.request.user, page=page):
            return

        current_page_menu = self.toolbar.get_or_create_menu("page")
        position = self.get_position(current_page_menu)

        file_formats = FILE_FORMATS.values()

        if len(file_formats) == 1:
            menu = current_page_menu
        else:
            menu = current_page_menu.get_or_create_menu(
                "export-page", _("Export"), position=position
            )

        for file_format in file_formats:
            label = _("Export to {ext}").format(ext="." + file_format.ext)
            url = reverse(
                "export-page:cms_page",
                kwargs={"page_pk": page.pk, "file_format": file_format.name},
            )
            menu.add_link_item(label, url=url, position=position)

        current_page_menu.add_break("export-page-break", position=position)

    def get_position(self, menu):
        # Last separator
        return menu.find_items(Break)[-1].index
