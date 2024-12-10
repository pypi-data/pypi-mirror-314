"""
Tests for the context processors
"""

# Standard Library
from unittest.mock import patch

# Django
from django.http import HttpRequest
from django.test import TestCase

# AA Templates: Terra Nanotech
from tnnt_templates.app_settings import AppSettings
from tnnt_templates.context_processors import tnnt_settings


class ContextProcessorsTests(TestCase):
    """
    Test the context processors
    """

    def setUp(self):
        """
        Setup tests

        :return:
        :rtype:
        """

        self.request = HttpRequest()

    def test_should_return_default_entity_id_when_not_set(self):
        """
        Test the default value of TNNT_TEMPLATE_ENTITY_ID

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_ENTITY_ID"], second=1)

    @patch.object(target=AppSettings, attribute="TNNT_TEMPLATE_ENTITY_ID", new=5)
    def test_should_return_custom_entity_id_when_set(self):
        """
        Test the custom value of TNNT_TEMPLATE_ENTITY_ID

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_ENTITY_ID"], second=5)

    def test_should_return_alliance_as_default_entity_type_when_not_set(self):
        """
        Test the default value of TNNT_TEMPLATE_ENTITY_TYPE

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_ENTITY_TYPE"], second="alliance")

    @patch.object(
        target=AppSettings, attribute="TNNT_TEMPLATE_ENTITY_TYPE", new="corporation"
    )
    def test_should_return_custom_entity_type_when_set(self):
        """
        Test the custom value of TNNT_TEMPLATE_ENTITY_TYPE

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(
            first=result["TNNT_TEMPLATE_ENTITY_TYPE"], second="corporation"
        )

    def test_should_return_empty_string_as_default_entity_name_when_not_set(self):
        """
        Test the default value of TNNT_TEMPLATE_ENTITY_NAME

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_ENTITY_NAME"], second="")

    @patch.object(
        target=AppSettings, attribute="TNNT_TEMPLATE_ENTITY_NAME", new="Starfleet"
    )
    def test_should_return_custom_entity_name_when_set(self):
        """
        Test the custom value of TNNT_TEMPLATE_ENTITY_NAME

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_ENTITY_NAME"], second="Starfleet")

    def test_should_not_include_own_websites_when_not_set(self):
        """
        Test the default value of TNNT_TEMPLATE_URLS_OWN_WEBSITES

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_URLS_OWN_WEBSITES"], second=[])

    @patch.object(
        target=AppSettings,
        attribute="TNNT_TEMPLATE_URLS_OWN_WEBSITES",
        new=["http://example.com"],
    )
    def test_should_include_custom_own_websites_when_set(self):
        """
        Test the custom value of TNNT_TEMPLATE_URLS_OWN_WEBSITES

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(
            first=result["TNNT_TEMPLATE_URLS_OWN_WEBSITES"],
            second=["http://example.com"],
        )

    def test_should_not_include_other_websites_when_not_set(self):
        """
        Test the default value of TNNT_TEMPLATE_URLS_OTHER_WEBSITES

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(first=result["TNNT_TEMPLATE_URLS_OTHER_WEBSITES"], second=[])

    @patch.object(
        target=AppSettings,
        attribute="TNNT_TEMPLATE_URLS_OTHER_WEBSITES",
        new=["http://example.com"],
    )
    def test_should_include_custom_other_websites_when_set(self):
        """
        Test the custom value of TNNT_TEMPLATE_URLS_OTHER_WEBSITES

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(
            first=result["TNNT_TEMPLATE_URLS_OTHER_WEBSITES"],
            second=["http://example.com"],
        )

    def test_should_return_the_aa_logo(self):
        """
        Test the default value of TNNT_TEMPLATE_AA_LOGO

        :return:
        :rtype:
        """

        result = tnnt_settings(request=self.request)

        self.assertEqual(
            first=result["TNNT_TEMPLATE_AA_LOGO"],
            second="/static/allianceauth/images/auth-logo.svg",
        )
