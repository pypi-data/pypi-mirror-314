"""
TN-NT Templates content processor
"""

# Django
from django.core.handlers.wsgi import WSGIRequest

# AA Templates: Terra Nanotech
from tnnt_templates.app_settings import AppSettings


def tnnt_settings(request: WSGIRequest) -> dict:  # pylint: disable=unused-argument
    """
    Returning a settings dict
    :param request:
    :return:
    """

    # AA logo
    return_value = {
        "TNNT_TEMPLATE_AA_LOGO": "/static/allianceauth/images/auth-logo.svg"
    }

    # entity ID
    # 1 if none is given
    try:
        return_value["TNNT_TEMPLATE_ENTITY_ID"] = AppSettings.TNNT_TEMPLATE_ENTITY_ID
    except AttributeError:
        return_value["TNNT_TEMPLATE_ENTITY_ID"] = 1

    # entity type
    # 'alliance' if none is given
    try:
        return_value["TNNT_TEMPLATE_ENTITY_TYPE"] = (
            AppSettings.TNNT_TEMPLATE_ENTITY_TYPE
        )
    except AttributeError:
        return_value["TNNT_TEMPLATE_ENTITY_TYPE"] = "alliance"

    # entity name
    # empty if none is given
    try:
        return_value["TNNT_TEMPLATE_ENTITY_NAME"] = (
            AppSettings.TNNT_TEMPLATE_ENTITY_NAME
        )
    except AttributeError:
        return_value["TNNT_TEMPLATE_ENTITY_NAME"] = ""

    try:
        return_value["TNNT_TEMPLATE_URLS_OWN_WEBSITES"] = (
            AppSettings.TNNT_TEMPLATE_URLS_OWN_WEBSITES
        )
    except AttributeError:
        pass

    try:
        return_value["TNNT_TEMPLATE_URLS_OTHER_WEBSITES"] = (
            AppSettings.TNNT_TEMPLATE_URLS_OTHER_WEBSITES
        )
    except AttributeError:
        pass

    return return_value
