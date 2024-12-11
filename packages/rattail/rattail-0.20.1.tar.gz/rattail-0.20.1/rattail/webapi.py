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
Generic web API client base class
"""

import json
import requests


class GenericWebAPI:
    """
    Generic base class for web API clients.
    """

    def __init__(
            self,
            config,
            base_url,
            max_retries=None,
            verify=None,
            **kwargs):

        self.config = config
        self.app = self.config.get_app()
        self.model = self.app.model

        self.session = requests.Session()

        self.base_url = base_url
        if self.base_url:
            self.base_url = self.base_url.rstrip('/')

        self.max_retries = max_retries
        if self.max_retries is not None:
            adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
            self.session.mount(self.base_url, adapter)

        if verify is not None:
            self.session.verify = verify

    def _request(self, request_method, api_method, params=None, data=None):
        """
        Perform a request for the given API method, and return the response.
        """
        api_method = api_method.lstrip('/')
        url = f'{self.base_url}/{api_method}'
        params = params or {}

        if request_method == 'GET':
            response = self.session.get(url, params=params)

        elif request_method == 'POST':
            kwargs = {'params': params}
            if data:
                kwargs['data'] = json.dumps(data)
            response = self.session.post(url, **kwargs)

        elif request_method == 'PATCH':
            kwargs = {'params': params}
            if data:
                kwargs['data'] = json.dumps(data)
            response = self.session.patch(url, **kwargs)

        elif request_method == 'DELETE':
            kwargs = {'params': params}
            if data:
                kwargs['data'] = json.dumps(data)
            response = self.session.delete(url, **kwargs)

        else:
            raise NotImplementedError(f"unknown request method: {request_method}")

        response.raise_for_status()
        return response

    def get(self, api_method, params=None):
        """
        Perform a GET request for the given API method, and return the response.
        """
        return self._request('GET', api_method, params=params)

    def post(self, api_method, params=None, data=None):
        """
        Perform a POST request for the given API method, and return the response.
        """
        return self._request('POST', api_method, params=params, data=data)

    def patch(self, api_method, params=None, data=None):
        """
        Perform a PATCH request for the given API method, and return the response.
        """
        return self._request('PATCH', api_method, params=params, data=data)

    def delete(self, api_method, params=None):
        """
        Perform a DELETE request for the given API method, and return the response.
        """
        return self._request('DELETE', api_method, params=params)
