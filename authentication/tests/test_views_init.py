import importlib
import os
import unittest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django


django.setup()


class AuthenticationViewsImportTests(unittest.TestCase):
    def test_import_authentication_views_package(self):
        module = importlib.import_module("authentication.views")
        self.assertTrue(hasattr(module, "RegisterViewSet"))
        self.assertTrue(hasattr(module, "LoginViewSet"))
