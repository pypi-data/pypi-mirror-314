import cgi
import os
import re
import secrets
import socket
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs

import pkce
import requests
from keystoneauth1 import access, exceptions
from keystoneauth1.identity import base

DEFAULT_OIDC_ENDPOINT = 'https://idp.apis.syseleven.de/realms/application/protocol/openid-connect'
DEFAULT_CLIENT_ID = 's11-user'
JWT_CACHE_PATH = os.path.expanduser('~/.config/openstack-s11auth/auth')
TIMEOUT = 60


class _CallbackServer(HTTPServer):
    """Local HTTP server for the OIDC redirect callback.

    This class implements a local HTTP server that will listen on a
    given port and process a single request.

    Required input parameters must be set by the caller after initialization."""

    # input parameters
    oidc_endpoint = None
    client_id = None
    req_state = None
    req_nonce = None
    code_challenge = None

    # output parameters
    code = None

    def server_bind(self):
        HTTPServer.server_bind(self)
        self.socket.settimeout(TIMEOUT)


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/auth':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            params = {
                'client_id': self.server.client_id,
                'redirect_uri': f'http://localhost:{self.server.server_port}',
                'response_type': 'code',
                'response_mode': 'form_post',
                'scope': 'openid',
                'state': self.server.req_state,
                'nonce': self.server.req_nonce,
                'code_challenge': self.server.code_challenge,
                'code_challenge_method': 'S256'
            }
            auth_url = f'{self.server.oidc_endpoint}/auth?{urlencode(params)}'

            self.wfile.write(
                b'<html><head><title>Authentication Redirect</title>'
                b'<meta http-equiv="refresh" content="0; url=' + str.encode(auth_url) + b'">'
                                                                                        b'</head><body></body></html>')

            return

        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Not found')

    def do_POST(self):
        try:
            post_data = {}
            content_type, params = cgi.parse_header(self.headers['content-type'])
            if content_type == 'multipart/form-data':
                post_data = cgi.parse_multipart(self.rfile, params)
            elif content_type == 'application/x-www-form-urlencoded':
                length = int(self.headers['content-length'])
                post_data = parse_qs(self.rfile.read(length), keep_blank_values=1)

            if b'code' not in post_data:
                raise AssertionError('Code not found in response')

            if b'state' not in post_data:
                raise AssertionError('State not found in response')

            if post_data[b'state'][0].decode() != self.server.req_state:
                raise AssertionError('State mismatch')

            self.server.code = post_data[b'code'][0].decode()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(
                b'<html><head><title>Authentication Status OK</title>'
                b'<script>window.close()</script></head>'
                b'<body><p>The authentication flow has been completed.</p>'
                b'<p>You can close this window.</p>'
                b'</body></html>')

        except AssertionError as e:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Bad request: {}'.format(e).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Internal server error: {}'.format(e).encode())

    def log_message(self, format, *args):
        # disable logging
        pass


class S11Auth(base.BaseIdentityPlugin):
    """Implementation for s11 authentication."""

    def __init__(self, auth_url, project_id="", redirect_port='8080', **kwargs):
        super(S11Auth, self).__init__(auth_url=auth_url)

        self.auth_url = auth_url
        self.project_id = project_id

        # URL of the redirect server (spawned by this plugin)
        self.redirect_port = int(redirect_port)
        self.auth_uri = f'http://localhost:{self.redirect_port}/auth'

        # PKCE parameters
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()

        # Keycloak parameters
        self.oidc_endpoint = os.environ.get("OIDC_ENDPOINT", DEFAULT_OIDC_ENDPOINT)
        self.client_id = os.environ.get("CLIENT_ID", DEFAULT_CLIENT_ID)

    @staticmethod
    def _get_jwt_from_cache():
        cache_dir = '/'.join(JWT_CACHE_PATH.split('/')[:-1])
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        if not os.path.exists(JWT_CACHE_PATH):
            return None

        with open(JWT_CACHE_PATH, 'r') as f:
            return f.readline()

    @staticmethod
    def _cache_jwt(jwt):
        with open(JWT_CACHE_PATH, 'w') as f:
            return f.write(jwt)

    def _jwt_to_access_info(self, jwt):
        payload = {
            "auth": {
                "identity": {
                    "methods": ["s11auth"],
                    "s11auth": {
                        "token": jwt,
                        "project_id": self.project_id,
                    }
                }
            }
        }
        if len(self.project_id) > 0:
            self._validate_project_id()
            payload['auth']['scope'] = {
                "project": {
                    "id": self.project_id,
                }
            }
        response = requests.post(f'{self.auth_url}/auth/tokens', json=payload)
        if response.status_code != 201:
            message = response.status_code
            if response.json().get('error'):
                message = response.json().get('error').get('message')
            if response.status_code == 401 and 'The request you have made requires authentication.' in message:
                raise exceptions.AuthorizationFailure(
                    f'Failed to get fernet token. Please ensure that you have the correct permissions to access the project {self.project_id}')
            raise exceptions.AuthorizationFailure(
                f'Failed to get fernet token (invalid response: HTTP {response.status_code}: {message})')

        return access.create(resp=response)

    def get_auth_ref(self, session, **kwargs):
        # try to get jwt from cache
        jwt = self._get_jwt_from_cache()
        jwt_is_new = False

        if jwt is None:
            # get a new jwt, if no cache available and cache afterward
            jwt = self._get_keycloak_token()
            self._cache_jwt(jwt)
            jwt_is_new = False

        try:
            return self._jwt_to_access_info(jwt)
        except exceptions.AuthorizationFailure:
            # if the jwt was from cache, try again with a new one
            if not jwt_is_new:
                jwt = self._get_keycloak_token()
                self._cache_jwt(jwt)
                return self._jwt_to_access_info(jwt)

    def _validate_project_id(self):
        if not re.compile(r'^[a-z0-9-]{32}$').match(self.project_id):
            raise Exception(
                f'Invalid project ID: {self.project_id} (must be lowercase alphanumeric without dashes)')

    def _get_keycloak_token(self):
        # generate random state and nonce
        self.state = secrets.token_urlsafe()
        self.nonce = secrets.token_urlsafe()

        # open browser and wait for the callback
        webbrowser.open(self.auth_uri, new=1, autoraise=True)
        code = self._wait_for_code()

        # exchange code for token
        response = requests.post(f'{self.oidc_endpoint}/token', data={
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'code': code,
            'redirect_uri': f'http://localhost:{self.redirect_port}',
            'code_verifier': self.code_verifier
        })
        if response.status_code != 200:
            raise Exception(f'Failed to get token (invalid response: HTTP {response.status_code}: {response.text})')

        json_response = response.json()
        if 'id_token' not in json_response:
            raise Exception('Failed to get token (missing id_token)')

        return json_response.get('id_token')

    def _wait_for_code(self):
        # spawn the callback server
        server_address = ('localhost', self.redirect_port)
        try:
            httpd = _CallbackServer(server_address, _CallbackHandler)
        except socket.error:
            print(f'Cannot spawn the callback server on port {self.redirect_port}, '
                  f'please specify a different port using the --os-redirect-port option.')
            raise

        # set the required parameters
        httpd.oidc_endpoint = self.oidc_endpoint
        httpd.client_id = self.client_id
        httpd.req_state = self.state
        httpd.req_nonce = self.nonce
        httpd.code_challenge = self.code_challenge

        # wait until the callback server processes the request and sent us the id_token
        start = int(time.time())
        while not httpd.code:
            if time.time() - start > TIMEOUT:
                raise Exception('Timeout waiting for authentication')
            httpd.handle_request()

        return httpd.code
