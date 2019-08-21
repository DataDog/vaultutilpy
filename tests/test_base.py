import vaultutilpy
import tempfile
import mock
import os

from unittest import TestCase


class TestBase(TestCase):
    def test_when_token_file_dne(self):
        os.environ["VAULT_ADDR"] = "test"
        os.environ["VAULT_AUTH_PATH"] = "test"
        os.environ["VAULT_ROLE"] = "test"

        vaultutilpy.KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE = "file-does-not-exists"
        with self.assertRaises(vaultutilpy.TokenFileNotFound):
            vaultutilpy.in_cluster_client()

    def test_when_envvars_dne(self):
        _, filename = tempfile.mkstemp()
        with mock.patch("vaultutilpy.base.KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE", filename):
            with self.assertRaises(vaultutilpy.MissingEnvVar):
                vaultutilpy.in_cluster_client()
