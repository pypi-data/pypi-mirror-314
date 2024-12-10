import unicodedata

from django.utils.html import strip_tags


def clean_value(value):
    """
    It would be better to use bleach.clean() as control chars as replaced
    by '? in bleach 2+.
    Requirement conflict: djangocms-text-ckeditor 3.6.0 needs
    html5lib<=0.9999999 but bleach needs the versions above that.
    Watch: https://github.com/divio/djangocms-text-ckeditor/issues/403
    """
    white_list = "\r\n"

    def is_control_char(char):
        return unicodedata.category(char).startswith("C")

    def valid_char(char):
        return not is_control_char(char) or char in white_list

    if isinstance(value, str):
        value = "".join(filter(valid_char, value))
        value = strip_tags(value).strip()
    return value
