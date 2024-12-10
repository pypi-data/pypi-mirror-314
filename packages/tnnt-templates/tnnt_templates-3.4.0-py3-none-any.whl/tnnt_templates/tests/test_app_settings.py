"""
Tests for the app settings
"""

# Standard Library
from unittest.mock import patch

# Django
from django.test import TestCase, modify_settings

# AA Templates: Terra Nanotech
from tnnt_templates.app_settings import AppSettings


class TestAppSettings(TestCase):
    """
    Test the app settings
    """

    def setUp(self):
        """
        Setup tests

        :return:
        :rtype:
        """

        self.app_settings = AppSettings()

    @modify_settings(INSTALLED_APPS={"append": "aagdpr"})
    def test_aagdpr_installed(self):
        """
        Test if the aagdpr app is installed

        :return:
        :rtype:
        """

        # app_settings = AppSettings()

        self.assertEqual(first=self.app_settings.aagdpr_installed(), second=True)

    @modify_settings(INSTALLED_APPS={"remove": "aagdpr"})
    def test_aagdpr_not_installed(self):
        """
        Test if the aagdpr app is not installed

        :return:
        :rtype:
        """

        self.assertEqual(first=self.app_settings.aagdpr_installed(), second=False)

    def test_TNNT_TEMPLATE_ENTITY_TYPE_default_value(self):
        """
        Test the default value of TNNT_TEMPLATE_ENTITY_TYPE

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_ENTITY_TYPE, second="alliance"
        )

    @patch.object(
        target=AppSettings, attribute="TNNT_TEMPLATE_ENTITY_TYPE", new="corporation"
    )
    def test_TNNT_TEMPLATE_ENTITY_TYPE_corporation(self):
        """
        Test the value of TNNT_TEMPLATE_ENTITY_TYPE when set to "corporation"

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_ENTITY_TYPE, second="corporation"
        )

    def should_return_default_TNNT_TEMPLATE_ENTITY_ID(self):
        """
        Test the default value of TNNT_TEMPLATE_ENTITY_ID

        :return:
        :rtype:
        """

        self.assertEqual(first=self.app_settings.TNNT_TEMPLATE_ENTITY_ID, second=1)

    @patch.object(target=AppSettings, attribute="TNNT_TEMPLATE_ENTITY_ID", new=2)
    def should_return_custom_TNNT_TEMPLATE_ENTITY_ID(self):
        """
        Test the custom value of TNNT_TEMPLATE_ENTITY_ID

        :return:
        :rtype:
        """

        self.assertEqual(first=self.app_settings.TNNT_TEMPLATE_ENTITY_ID, second=2)

    def should_return_default_TNNT_TEMPLATE_ENTITY_NAME(self):
        """
        Test the default value of TNNT_TEMPLATE_ENTITY_NAME

        :return:
        :rtype:
        """

        self.assertEqual(first=self.app_settings.TNNT_TEMPLATE_ENTITY_NAME, second="")

    @patch.object(
        target=AppSettings, attribute="TNNT_TEMPLATE_ENTITY_NAME", new="Test Name"
    )
    def should_return_custom_TNNT_TEMPLATE_ENTITY_NAME(self):
        """
        Test the custom value of TNNT_TEMPLATE_ENTITY_NAME

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_ENTITY_NAME, second="Test Name"
        )

    def should_return_default_TNNT_TEMPLATE_URLS_OWN_WEBSITES(self):
        """
        Test the default value of TNNT_TEMPLATE_URLS_OWN_WEBSITES

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_URLS_OWN_WEBSITES, second=[]
        )

    @patch.object(
        target=AppSettings,
        attribute="TNNT_TEMPLATE_URLS_OWN_WEBSITES",
        new=["http://example.com"],
    )
    def should_return_custom_TNNT_TEMPLATE_URLS_OWN_WEBSITES(self):
        """
        Test the custom value of TNNT_TEMPLATE_URLS_OWN_WEBSITES

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_URLS_OWN_WEBSITES,
            second=["http://example.com"],
        )

    def should_return_default_TNNT_TEMPLATE_URLS_OTHER_WEBSITES(self):
        """
        Test the default value of TNNT_TEMPLATE_URLS_OTHER_WEBSITES

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_URLS_OTHER_WEBSITES, second=[]
        )

    @patch.object(
        target=AppSettings,
        attribute="TNNT_TEMPLATE_URLS_OTHER_WEBSITES",
        new=["http://example.com"],
    )
    def should_return_custom_TNNT_TEMPLATE_URLS_OTHER_WEBSITES(self):
        """
        Test the custom value of TNNT_TEMPLATE_URLS_OTHER_WEBSITES

        :return:
        :rtype:
        """

        self.assertEqual(
            first=self.app_settings.TNNT_TEMPLATE_URLS_OTHER_WEBSITES,
            second=["http://example.com"],
        )
