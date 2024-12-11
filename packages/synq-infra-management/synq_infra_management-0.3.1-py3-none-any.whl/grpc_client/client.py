import time

import grpc
from grpc import AuthMetadataPlugin
from oauthlib.oauth2 import LegacyApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


class TokenAuth(AuthMetadataPlugin):
    def __init__(self, token_source):
        self._token_source = token_source

    def __call__(self, context, callback):
        try:
            token = self._token_source.get_token()
            callback([("authorization", f"Bearer {token}")], None)
        except Exception as e:
            callback(None, e)


class TokenSource:
    def __init__(self, long_lived_token, api_endpoint="developer.synq.io"):
        self.api_endpoint = api_endpoint
        self.long_lived_token = long_lived_token
        self.token_url = f"https://{self.api_endpoint}/oauth2/token"
        self.token = self.obtain_token()

    def obtain_token(self):
        client = LegacyApplicationClient(client_id="synq")
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=self.token_url,
            username="synq",
            password=self.long_lived_token,
            auth=HTTPBasicAuth("synq", self.long_lived_token),
        )
        return token

    def get_token(self):
        expires_at = self.token["expires_in"] + time.time()
        is_expired = time.time() >= expires_at
        if is_expired:
            self.token = self.obtain_token()
        return self.token["access_token"]


def long_lived_token_source(long_lived_token, api_endpoint="developer.synq.io"):
    try:
        return TokenSource(long_lived_token, api_endpoint)
    except Exception as e:
        raise ValueError(f"Error obtaining token: {e}")


def get_grpc_channel(long_lived_token, api_endpoint="developer.synq.io"):
    token_source = long_lived_token_source(long_lived_token, api_endpoint)
    auth_plugin = TokenAuth(token_source)
    grpc_credentials = grpc.metadata_call_credentials(auth_plugin)
    channel = grpc.secure_channel(
        "developer.synq.io:443",
        grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(), grpc_credentials
        ),
        options=(("grpc.default_authority", api_endpoint),),
    )
    return channel
