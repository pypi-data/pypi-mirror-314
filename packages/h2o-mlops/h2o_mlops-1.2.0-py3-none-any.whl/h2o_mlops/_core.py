from __future__ import annotations

import os
import ssl
from typing import Optional
from urllib.parse import urlparse

import certifi
import h2o_authn
import h2o_discovery

import h2o_mlops_autogen
from h2o_mlops import _connectors, _projects
from h2o_mlops import _runtimes


class Client:
    """Connect to and interact with H2O MLOps.

    Args:
        gateway_url: full URL of the MLOps gRPC Gateway to connect to
            (needed when passing a token_provider)
        h2o_cloud_url: full URL of the H2O Cloud to connect to
            (needed when passing a refresh_token)
        refresh_token: client refresh token retrieved from H2O Cloud
            (needed when passing a h2o_cloud_url)
        token_provider: authentication token to authorize access on H2O AI Cloud
            (needed when passing a gateway_url)
        verify_ssl: (Optional) Enables SSL/TLS verification. Set this as False
            to skip SSL certificate verification when calling the API from
            an HTTPS server. Defaults to True.
        ssl_cacert: (Optional) Path to a custom certificate file for verifying
            the peer's SSL/TLS certificate.

    Examples::

        ### Connect from H2O Cloud notebook
        ### (credentials are automatically discovered and used)

        mlops = h2o_mlops.Client()

        ### Connect with h2o_cloud_url and refresh_token

        mlops = h2o_mlops.Client(
            h2o_cloud_url="https://...",
            refresh_token="eyJhbGciOiJIUzI1N...",
        )

        ### Connect with gateway_url and token_provider

        # 1) set up a token provider with a refresh token from AI Cloud
        token_provider = h2o_authn.TokenProvider(
            refresh_token="eyJhbGciOiJIUzI1N...",
            client_id="python_client",
            token_endpoint_url="https://keycloak-server/auth/realms/..."
        )

        # 2) use the token provider to get authorization to connect to the
        # MLOps API
        mlops = h2o_mlops.Client(
            gateway_url="https://mlops-api.my.domain",
            token_provider=token_provider
        )
    """

    def __init__(
        self,
        gateway_url: Optional[str] = None,
        token_provider: Optional[h2o_authn.TokenProvider] = None,
        h2o_cloud_url: Optional[str] = None,
        refresh_token: Optional[str] = None,
        verify_ssl: bool = True,
        ssl_cacert: Optional[str] = None,
    ):
        self._backend = None
        self._discovery = None
        self._token_provider = None

        self._ssl_context = ssl.SSLContext()
        self._ssl_context.verify_mode = (
            ssl.CERT_REQUIRED if verify_ssl else ssl.CERT_NONE
        )
        self._ssl_context.load_verify_locations(
            cafile=(
                ssl_cacert
                or os.getenv("MLOPS_AUTH_CA_FILE_OVERRIDE")
                or certifi.where()
            )
        )

        if gateway_url and token_provider:
            self._backend = h2o_mlops_autogen.Client(
                gateway_url=gateway_url,
                token_provider=token_provider,
                verify_ssl=verify_ssl,
                ssl_cacert=ssl_cacert,
            )
            return

        if h2o_cloud_url:
            self._h2o_cloud_url = urlparse(h2o_cloud_url)
            self._discovery = h2o_discovery.discover(
                environment=h2o_cloud_url,
                ssl_context=self._ssl_context,
            )
        else:
            self._discovery = h2o_discovery.discover(ssl_context=self._ssl_context)

        self._token_provider = h2o_authn.TokenProvider(
            refresh_token=refresh_token or os.getenv("H2O_CLOUD_CLIENT_PLATFORM_TOKEN"),
            issuer_url=self._discovery.environment.issuer_url,
            client_id=self._discovery.clients["platform"].oauth2_client_id,
            http_ssl_context=self._ssl_context,
        )

        self._backend = h2o_mlops_autogen.Client(
            gateway_url=self._discovery.services["mlops-api"].uri,
            token_provider=self._token_provider,
            verify_ssl=verify_ssl,
            ssl_cacert=ssl_cacert,
        )

    @property
    def projects(self) -> _projects.MLOpsProjects:
        """Interact with Projects in H2O MLOps"""
        return _projects.MLOpsProjects(self)

    @property
    def runtimes(self) -> _runtimes.MLOpsRuntimes:
        """Interact with Scoring Runtimes in H2O MLOps"""
        return _runtimes.MLOpsRuntimes(self)

    @property
    def batch_connectors(self) -> _connectors.MLOpsBatchConnectors:
        """Interact with Batch Scoring Connectors in H2O MLOps"""
        return _connectors.MLOpsBatchConnectors(self)

    def _get_username(self, user_id: str) -> str:
        """Get user display name from internal ID."""
        return self._backend.storage.user.get_user(
            h2o_mlops_autogen.StorageGetUserRequest(id=user_id)
        ).user.username
