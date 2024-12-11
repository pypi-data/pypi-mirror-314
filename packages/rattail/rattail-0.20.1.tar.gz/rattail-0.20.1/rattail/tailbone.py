# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Tailbone API Client
"""

import json
import logging
from urllib.parse import urlparse

import requests


log = logging.getLogger(__name__)


class TailboneAPIClient(object):
    """
    Simple client for Tailbone web API.

    :param base_url: Base URL of the Tailbone API.  Usually this is
       something like ``'http://my.example.com/api'`` although YMMV.

       If you have a default URL configured as below then you do not
       need to provide a ``base_url`` to this class.

       .. code-block:: ini

          [tailbone.api]
          base_url = http://my.example.com/api

    :param max_retries: Maximum number of retries each connection
       should attempt.  This value is ultimately given to the
       :class:`~requests:requests.adapters.HTTPAdapter` instance.

       Instead of specifying this value via constructor you can add it
       to your config:

       .. code-block:: ini

          [tailbone.api]
          max_retries = 5
    """
    session = None
    logged_in = False

    def __init__(self, config, base_url=None, max_retries=None, **kwargs):
        self.config = config

        self.base_url = base_url or self.config.require(
            'tailbone.api', 'base_url')
        self.base_url = self.base_url.rstrip('/')

        if max_retries is not None:
            self.max_retries = max_retries
        else:
            self.max_retries = self.config.getint('tailbone.api', 'max_retries')

    def _init(self):
        if self.session:
            return

        self.session = requests.Session()

        # maybe *disable* SSL cert verification
        # (should only be used for testing! e.g. w/ self-signed certs)
        if not self.config.getbool('tailbone.api', 'ssl_verify', default=True):
            self.session.verify = False

        # maybe set max retries, e.g. for flaky connections
        if self.max_retries is not None:
            adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
            self.session.mount(self.base_url, adapter)

        # TODO: is this a good idea, or hacky security risk..?
        # without it, can get error response:
        # 400 Client Error: Bad CSRF Origin for url
        parts = urlparse(self.base_url)
        self.session.headers.update({
            'Origin': f'{parts.scheme}://{parts.netloc}',
        })

        # fetch basic 'session' endpoint, to get current xsrf token
        # (this does not require any authentication, which is next)
        response = self.get('/session')
        self.session.headers.update({
            'X-XSRF-TOKEN': response.cookies['XSRF-TOKEN']})

        # authenticate via token (preferred), or user/pass login
        token = self.config.get('tailbone.api', 'token')
        if token:
            self.session.headers.update({
                'Authorization': 'Bearer {}'.format(token),
            })
        else: # no token, so attempt login w/ credentials
            if not self.login():
                raise RuntimeError("login failed! (consider using token auth)")

    def _request(self, request_method, api_method, params=None, data=None):
        """
        Perform a request for the given API method, and return the response.
        """
        api_method = api_method.lstrip('/')
        url = '{}/{}'.format(self.base_url, api_method)
        if request_method == 'GET':
            response = self.session.get(url, params=params)
        elif request_method == 'POST':
            response = self.session.post(url, params=params,
                                         data=json.dumps(data))
        else:
            raise NotImplementedError("unknown request method: {}".format(
                request_method))
        response.raise_for_status()
        return response

    def get(self, api_method, params=None):
        """
        Perform a GET request for the given API method, and return the response.
        """
        self._init()
        return self._request('GET', api_method, params=params)

    def post(self, api_method, **kwargs):
        """
        Perform a POST request for the given API method, and return the response.
        """
        self._init()
        return self._request('POST', api_method, **kwargs)

    def login(self, username=None, password=None):
        if self.logged_in:
            return True

        if not username:
            username = self.config.require('tailbone.api', 'login.username')
        if not password:
            password = self.config.require('tailbone.api', 'login.password')

        response = self.post('/login', data={'username': username,
                                             'password': password})

        # ok means success
        data = response.json()
        if data.get('ok'):
            self.logged_in = True
            return True

        # log what we can if failure
        if data.get('error'):
            log.error("login failed: %s", data['error'])
        else:
            log.error("login failed somehow, please investigate")
        return False
