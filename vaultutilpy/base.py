import os
import hvac
import requests

__all__ = [
    'VaultutilpyError',
    'MissingEnvVar',
    'AuthTokenRetrieval',
    'SecretNotFound',
    'TokenFileNotFound',
    'in_cluster_client',
    'in_cluster_client'
]


class VaultutilpyError(Exception): pass
class MissingEnvVar(VaultutilpyError): pass
class AuthTokenRetrieval(VaultutilpyError): pass
class SecretNotFound(VaultutilpyError): pass
class TokenFileNotFound(VaultutilpyError): pass


KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE = "/var/run/secrets/kubernetes.io/serviceaccount/token"


def in_cluster_client():
    """
    in_cluster_client returns a vault (hvac) API client using environment variables passed
    to pods within a kubernetes cluster
    """
    for envvar in ["VAULT_ADDR", "VAULT_AUTH_PATH", "VAULT_ROLE"]:
        if os.environ.get(envvar) is None:
            raise MissingEnvVar("Missing Envvar: {0}".format(envvar))

    vault_addr = os.environ.get("VAULT_ADDR")
    vault_auth_path = os.environ.get("VAULT_AUTH_PATH")
    vault_role = os.environ.get("VAULT_ROLE")

    if not os.path.exists(KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE):
        raise TokenFileNotFound("Could not find serviceaccount token at {0}".
                format(KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE))

    with open(KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE, "rb") as fd:
        jwt = fd.read()

    payload = {"jwt": jwt, "role": vault_role}
    auth_url = "{0}/v1/auth/{1}/login".format(vault_addr, vault_auth_path)
    req = requests.post(auth_url, data=payload)
    if req.status_code != requests.codes.ok:
        raise AuthTokenRetrieval("Failed to receive auth token with code: {0} err: {1}".format(req.status_code, req.text))

    client_token = req.json().get('auth', {}).get('client_token', False)
    if not client_token:
        raise AuthTokenRetrieval("Failed to parse auth token")

    client = hvac.Client(url=vault_addr, token=client_token)
    return client


def in_cluster_secret(path, field):
    """
    in_cluster_secret is a helper function to retrieve a secret from vault from within kubernetes
    """
    client = in_cluster_client()
    secret = client.read(path)
    if secret is None:
        raise SecretNotFound("Could not find secret path at path: {0}, field: {1}".format(path, field))
    val = secret.get(field, None)
    if val is None:
        raise SecretNotFound("Could not find secret field at path: {0}, field: {1}".format(path, field))
    return val
