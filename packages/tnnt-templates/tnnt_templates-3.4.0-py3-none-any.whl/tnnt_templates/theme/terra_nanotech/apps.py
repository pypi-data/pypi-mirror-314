"""
AppConfig for Terra Nanotech theme.
"""

# Django
from django.apps import AppConfig


class TerraNanotechThemeConfig(AppConfig):
    """
    AppConfig for Terra Nanotech theme.
    """

    name = "tnnt_templates.theme.terra_nanotech"
    label = "terra_nanotech"
    version = "5.3.2"
    verbose_name = f"Terra Nanotech v{version}"

    def ready(self):
        """
        Ready

        :return:
        :rtype:
        """

        pass  # pylint: disable=unnecessary-pass
