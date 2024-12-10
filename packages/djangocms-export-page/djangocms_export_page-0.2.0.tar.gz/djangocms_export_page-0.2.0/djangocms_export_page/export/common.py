from collections import namedtuple

from django.contrib.sites.shortcuts import get_current_site
from django.db.models import CharField, ForeignKey, TextField

from cms.models import CMSPlugin, Placeholder, StaticPlaceholder
from cms.models.fields import PlaceholderField
from djangocms_page_meta.utils import get_page_meta

from djangocms_export_page import settings

from ..utils import clean_value

Section = namedtuple("Section", ["name", "section", "components"])
Component = namedtuple("Component", ["name", "instance", "fields"])
Field = namedtuple("Field", ["name", "value"])

META_FIELD_BLACKLIST = ["_url"]


class PageExport:
    """
    1. CMS Page don't need any extra configuration to work.

    2. If a Plugin has a ForeignKey that would behave like children,
    add the following to the CMSPlugin model class:

        _export_page = {
            'children': 'items'
        }

    where 'items' is a iterable attribute of the model class.
    And for on the ForeignKey Django model class:

        _export_page = {
            'fields': ['name', ... ]
        }

    3. If you need to export a Django model included in a AppHook,
    add the following to the model class:

        _export_page = {
            'sections': [{
                'name': 'Meta',
                'fields': ['title', ... ]
            }, {
                'name': 'Body',
                'fields': ['content']
            }],
        }

    It's better to put the PlaceholderField (here `content`) in a separate section.
    """

    FIELD_FILTERS = {
        "is_content": lambda f: isinstance(
            f, (CharField, TextField, PlaceholderField, ForeignKey)
        ),
        "is_not_choice": lambda f: not f.choices,
        "is_not_slug": lambda f: f.name != "slug",
        "is_not_link": lambda f: not f.name.endswith("_link"),
    }

    def __init__(self, request, obj, language=None):
        self.request = request
        self.object = obj
        self.language = language
        self.base_url = self.get_base_url()
        self.page_url = self.get_page_url()
        self.page_meta = self.determine_meta_attributes(request, obj, language)

    def determine_meta_attributes(self, request, obj, language):
        page_meta = {}
        try:  # If a Django CMS page
            meta_dict = get_page_meta(obj, language).__dict__
        except AttributeError:
            try:  # If a Model object that uses the ModelMeta-mixin
                meta_dict = obj.get_meta(request)
            except Exception:
                meta_dict = {}

        # <meta property="some" content="value"> --> {'some (property)': value}
        page_meta.update(
            {
                "{} ({})".format(name, attr): value
                for attr, name, value in meta_dict.pop("extra_custom_props", [])
            }
        )

        for key, value in meta_dict.items():
            if type(value) is list:
                page_meta[key] = ",".join(value)
            if type(value) is str and key not in META_FIELD_BLACKLIST:
                page_meta[key] = value
        return page_meta

    def get_base_url(self):
        return "{protocol}://{domain}".format(
            protocol="https" if self.request.is_secure() else "http",
            domain=get_current_site(self.request).domain,
        )

    def get_page_url(self):
        return "{domain}{url}".format(
            domain=self.get_base_url(), url=self.object.get_absolute_url(self.language)
        )

    def export(self):
        raise NotImplementedError

    def filter_fields(self, fields):
        def can_be_exported(field):
            return all((test(field) for test in self.FIELD_FILTERS.values()))

        return filter(can_be_exported, fields)

    def get_data(self):
        sections = self.get_sections()

        for name, section, components in sections:
            if isinstance(section, Placeholder):
                placeholder = section
                plugins = self.get_ordered_plugins(placeholder, self.language)
                for plugin in plugins:
                    components.extend(self.get_components(plugin))
            elif isinstance(section, StaticPlaceholder):
                placeholder = section
                plugins = self.get_ordered_plugins(placeholder.public, self.language)
                for plugin in plugins:
                    components.extend(self.get_components(plugin))

        return [s for s in sections if s.components]

    # 1. Section

    def get_section_name(self, placeholder=None):
        return placeholder.get_label()

    def get_sections(self):
        sections = []
        if hasattr(self.object, "get_placeholders"):
            sections.extend(self.get_placeholders())
        if hasattr(self.object, "_export_page"):
            for section in self.object._export_page["sections"]:
                sections.append(
                    Section(
                        section["name"],
                        self.object,
                        self.get_defined_components(self.object, section["fields"]),
                    )
                )
        if hasattr(self.object, "template"):
            codes = settings.EXPORT_STATIC_PLACEHOLDERS.get(self.object.template)
            if codes:
                queryset = StaticPlaceholder.objects.filter(code__in=codes)
                sections.extend(self.get_static_placeholders(queryset))

        if self.page_meta:
            sections.append(
                Section(
                    "Page meta-data",
                    None,
                    components=[
                        Component(
                            "meta",
                            None,
                            fields=[
                                Field(key, value)
                                for key, value in self.page_meta.items()
                            ],
                        )
                    ],
                )
            )
        return sections

    def get_placeholders(self):
        placeholders = []

        for (
            declared_placeholder
        ) in self.object.get_declared_placeholders():  # to always get the correct order
            placeholder = self.object.get_placeholders(self.language).get(
                slot=declared_placeholder.slot
            )
            name = self.get_section_name(placeholder)
            # Weird way to sort placeholders:
            if "header" in placeholder.slot:
                placeholders.insert(0, Section(name, placeholder, []))
            else:
                placeholders.append(Section(name, placeholder, []))

        return placeholders

    def get_static_placeholders(self, static_placeholders):
        placeholders = []

        for placeholder in static_placeholders:
            placeholders.append(Section(placeholder.get_name(), placeholder, []))

        return placeholders

    @classmethod
    def get_ordered_plugins(cls, placeholder, language=None):
        yield from cls.next_plugin(
            [
                CMSPlugin.objects.get(pk=pk)
                for pk in placeholder.get_plugin_tree_order(language)
            ]
        )

    @classmethod
    def next_plugin(cls, plugins):
        for plugin in plugins:
            yield plugin
            yield from cls.next_plugin(plugin.get_children())

    # 2. Components

    def get_component_name(self, instance=None, plugin=None):
        name = plugin.name if plugin else instance._meta.verbose_name
        return "{}: {}".format(name, instance)

    def get_components(self, obj):
        components = []

        try:
            instance, plugin = obj.get_plugin_instance()
        except AttributeError:
            # obj is a regular Django model instance
            instance, plugin = None, None
        if instance and plugin:
            components.append(
                Component(
                    self.get_component_name(instance, plugin=plugin),
                    instance,
                    self.get_fields_with_values(instance, self.get_fields(instance)),
                )
            )

        if hasattr(obj, "_export_page"):
            children_attr = obj._export_page.get("children", "")
            for child in getattr(obj, children_attr, []):
                components.extend(self.get_defined_components(child))
                components.extend(self.get_components(child))
        elif hasattr(instance, "_export_page"):
            children_attr = instance._export_page.get("children", "")
            for child in getattr(instance, children_attr, []):
                components.extend(self.get_defined_components(child))
                components.extend(self.get_components(child))

        return components

    def get_defined_components(self, obj, field_names=None):
        """
        Gets components on a regular Django model object that are
        defined under `_export_page['fields']`.
        Usually returns one component, but can return one compontent for each Plugin
        in the placeholder fields.
        """
        field_names = field_names if field_names else obj._export_page["fields"]
        model_fields = {f.name: f for f in obj._meta.fields}
        fields = [(name, model_fields[name]) for name in field_names]

        regular_fields = [f for f in fields if not isinstance(f[1], PlaceholderField)]
        placeholder_fields = [f for f in fields if isinstance(f[1], PlaceholderField)]

        components = [
            Component(
                self.get_component_name(obj),
                obj,
                self.get_fields_with_values(obj, regular_fields),
            )
        ]

        for field_name, field in placeholder_fields:
            placeholder = getattr(obj, field_name)
            plugins = self.get_ordered_plugins(placeholder, self.language)
            for plugin in plugins:
                components.extend(self.get_components(plugin))

        return components

    # 3. Fields

    def get_fields_with_values(self, instance, fields):
        fields_with_values = []
        for field_name, field in fields:
            if field.many_to_one or field.one_to_one:
                relation = getattr(instance, field_name)
                if relation:
                    for relation_field in relation._meta.fields:
                        if (
                            hasattr(relation, "_export_page_field_names")
                            and relation_field.name in relation._export_page_field_names
                        ):
                            value = getattr(relation, relation_field.name)
                            cleaned_data = clean_value(value)
                            if cleaned_data is not None:
                                fields_with_values.append(
                                    Field(relation_field.verbose_name, cleaned_data)
                                )
            else:
                value = getattr(instance, field_name)
                cleaned_data = clean_value(value)
                if cleaned_data is not None:
                    fields_with_values.append(Field(field.verbose_name, cleaned_data))
        return fields_with_values

    def get_fields(self, instance):
        fields = self.get_custom_fields(instance)
        return ((field.name, field) for field in fields)

    def get_custom_fields(self, instance):
        base_fields = self.get_base_fields(instance)
        fields = (f for f in instance._meta.fields if f.name not in base_fields)
        return self.filter_fields(fields)

    def get_base_fields(self, instance):
        is_regular_cms_plugin = hasattr(instance, "cmsplugin_ptr")

        if is_regular_cms_plugin:
            fields = instance.cmsplugin_ptr._meta.fields
            yield "cmsplugin_ptr"
        else:
            fields = instance._meta.fields

        for field in fields:
            yield field.name
