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
Telemetry logic
"""

import os
import re
import subprocess
import warnings

from rattail.app import GenericHandler
from rattail.config import ConfigProfile
from rattail.tailbone import TailboneAPIClient


class TelemetryHandler(GenericHandler):
    """
    Handler for telemetry data
    """

    def get_profile(self, profile):
        if isinstance(profile, TelemetryProfile):
            return profile

        return TelemetryProfile(self.config, profile or 'default')

    def collect_all_data(self, profile=None, **kwargs):
        data = {}
        profile = self.get_profile(profile)

        for key in profile.collect_keys:
            collector = getattr(self, 'collect_data_{}'.format(key))
            data[key] = collector(profile=profile)

        self.normalize_errors(data)
        return data

    def collect_data_composer(self, profile, **kwargs):
        data = {}
        errors = []

        # executable
        composer = profile._config_string('collect.composer.executable')
        if not composer:
            composer = self.app.get_composer_executable()
        data['executable'] = composer

        # release
        try:
            output = subprocess.check_output([composer, '--version'])
        except subprocess.CalledProcessError:
            errors.append("Failed to execute `composer --version`")
        else:
            output = output.decode('utf_8').strip()
            data['release_full'] = output
            match = re.match(r'^Composer version (\d+\.\d+\.\d+)\s', output)
            if match:
                data['release_version'] = match.group(1)
            else:
                errors.append("Failed to parse Composer version")

        if errors:
            data['errors'] = errors
        return data

    # TODO: this probably belongs in rattail-corepos but we can move
    # it if/when telemetry is refactored for more dynamic profiles
    def collect_data_corepos(self, profile, **kwargs):
        data = {}
        errors = []

        # path (required for others to work)
        path = profile._config_string('collect.corepos.path')
        if not path:
            errors.append("No path configured!")
        else:
            data['path'] = path

            # owner
            try:
                output = subprocess.check_output([
                    'bash', '-c',
                    "ls -ld '{}' | cut -d ' ' -f 3,4".format(path)])
            except subprocess.CalledProcessError:
                errors.append("Failed to check path ownership")
            else:
                output = output.decode('utf_8').strip()
                data['owner'] = output

            # git_origin
            try:
                output = subprocess.check_output([
                    'bash', '-c',
                    "cd {} && git remote get-url origin".format(path)])
            except subprocess.CalledProcessError:
                errors.append("Failed to execute `git remote`")
            else:
                output = output.decode('utf_8').strip()
                data['git_origin'] = output

            # git_described
            try:
                output = subprocess.check_output([
                    'bash', '-c',
                    "cd {} && git describe --tags".format(path)])
            except subprocess.CalledProcessError:
                errors.append("Failed to execute `git describe`")
            else:
                output = output.decode('utf_8').strip()
                data['git_described'] = output

            # git_status
            try:
                output = subprocess.check_output([
                    'bash', '-c',
                    "cd {} && git status --branch --porcelain".format(path)])
            except subprocess.CalledProcessError:
                errors.append("Failed to execute `git status`")
            else:
                output = output.decode('utf_8').strip()
                data['git_status'] = output

            # composer = self.app.get_composer_executable()

            # # composer_status
            # try:
            #     output = subprocess.check_output([
            #         'bash', '-c',
            #         "cd {} && {} status".format(path, composer)
            #     ], stderr=subprocess.STDOUT)
            # except subprocess.CalledProcessError:
            #     errors.append("Failed to execute `composer status`")
            # else:
            #     output = output.decode('utf_8').strip()
            #     data['composer_status'] = output

            # # composer_validate
            # try:
            #     output = subprocess.check_output([
            #         'bash', '-c',
            #         "cd {} && {} validate".format(path, composer)
            #     ], stderr=subprocess.STDOUT)
            # except subprocess.CalledProcessError:
            #     errors.append("Failed to execute `composer validate`")
            # else:
            #     output = output.decode('utf_8').strip()
            #     data['composer_validated'] = output

        if errors:
            data['errors'] = errors
        return data

    def collect_data_git(self, profile, **kwargs):
        data = {}
        errors = []

        # executable
        git = profile._config_string('collect.git.executable',
                                     default='git')
        data['executable'] = git

        # release
        try:
            output = subprocess.check_output([git, '--version'])
        except subprocess.CalledProcessError:
            errors.append("Failed to execute `git --version`")
        else:
            output = output.decode('utf_8').strip()
            data['release_full'] = output
            match = re.match(r'^git version (\d+\.\d+\.\d+)', output)
            if match:
                data['release_version'] = match.group(1)
            else:
                errors.append("Failed to parse Git version")

        if errors:
            data['errors'] = errors
        return data

    def collect_data_mysql(self, profile, **kwargs):
        data = {}
        errors = []

        # release
        try:
            output = subprocess.check_output(['mysql', '--version'])
        except subprocess.CalledProcessError:
            errors.append("Failed to execute `mysql --version`")
        else:
            output = output.decode('utf_8').strip()
            data['release_full'] = output

            if 'mariadb' in output.lower():
                data['release_id'] = 'mariadb'
                match = re.match(r'^.*\s(\d+(?:\.\d+)+)-MariaDB', output)
                if match:
                    data['release_version'] = match.group(1)
                else:
                    errors.append("Failed to parse MariaDB version")
            else:
                data['release_id'] = 'mysql'
                match = re.match(r'^mysql\s+Ver (\d+(?:\.\d+)+)-', output)
                if match:
                    data['release_version'] = match.group(1)
                else:
                    errors.append("Failed to parse MySQL version")

        if errors:
            data['errors'] = errors
        return data

    def collect_data_os(self, profile, **kwargs):
        data = {}
        errors = []

        # release
        try:
            with open('/etc/os-release', 'rt') as f:
                output = f.read()
        except:
            errors.append("Failed to read /etc/release")
        else:
            release = {}
            pattern = re.compile(r'^([^=]+)=(.*)$')
            for line in output.strip().split('\n'):
                match = pattern.match(line)
                if match:
                    key, val = match.groups()
                    if val.startswith('"') and val.endswith('"'):
                        val = val.strip('"')
                    release[key] = val
            try:
                data['release_id'] = release['ID']
                data['release_version'] = release['VERSION_ID']
                data['release_full'] = release['PRETTY_NAME']
            except KeyError:
                errors.append("Failed to parse /etc/os-release")

        # timezone
        try:
            with open('/etc/timezone', 'rt') as f:
                output = f.read()
        except:
            errors.append("Failed to read /etc/timezone")
        else:
            data['timezone'] = output.strip()

        if errors:
            data['errors'] = errors
        return data

    def collect_data_php(self, profile, **kwargs):
        data = {}
        errors = []

        # release
        try:
            output = subprocess.check_output(['php', '--version'])
        except subprocess.CalledProcessError:
            errors.append("Failed to execute `php --version`")
        else:
            output = output.decode('utf_8').strip()
            data['release_full'] = output
            match = re.match(r'^PHP (\d+\.\d+\.\d+)-', output)
            if match:
                data['release_version'] = match.group(1)
            else:
                errors.append("Failed to parse PHP version")

        if errors:
            data['errors'] = errors
        return data

    def collect_data_postgresql(self, profile, **kwargs):
        data = {}
        errors = []

        # release
        try:
            output = subprocess.check_output(['psql', '--version'])
        except subprocess.CalledProcessError:
            errors.append("Failed to execute `psql --version`")
        else:
            output = output.decode('utf_8').strip()
            data['release_full'] = output
            match = re.match(r'^psql \(PostgreSQL\) (\d+\.\d+) ', output)
            if match:
                data['release_version'] = match.group(1)
            else:
                errors.append("Failed to parse PostgreSQL version")

        if errors:
            data['errors'] = errors
        return data

    def collect_data_python(self, profile, **kwargs):
        data = {}
        errors = []

        # envroot (required for others to work)
        envroot = profile._config_string('collect.python.envroot')
        if not envroot:
            errors.append("No envroot configured!")
        else:
            data['envroot'] = envroot

            # release
            python = os.path.join(envroot, 'bin/python')
            try:
                output = subprocess.check_output([python, '--version'])
            except subprocess.CalledProcessError:
                errors.append("Failed to execute `python --version`")
            else:
                output = output.decode('utf_8').strip()
                data['release_full'] = output
                match = re.match(r'^Python (\d+\.\d+\.\d+)', output)
                if match:
                    data['release_version'] = match.group(1)
                else:
                    errors.append("Failed to parse Python version")

        if errors:
            data['errors'] = errors
        return data

    def collect_data_rattail(self, profile, **kwargs):
        pass

    def normalize_errors(self, data, **kwargs):
        all_errors = []
        for key, value in data.items():
            if value:
                errors = value.pop('errors', None)
                if errors:
                    all_errors.extend(errors)
        if all_errors:
            data['errors'] = all_errors

    def submit_all_data(self, data, profile=None, **kwargs):
        profile = self.get_profile(profile)

        # TODO: any need for other types of submit logic?
        self.submit_data_tailbone_api(data, profile)

    def submit_data_tailbone_api(self, data, profile, **kwargs):
        api = TailboneAPIClient(self.config)

        data['uuid'] = profile.submit_uuid
        api.post(profile.submit_url, data=data)


class TelemetryProfile(ConfigProfile):
    """
    Holds configuration for a specific "profile" for use with
    telemetry.
    """
    section = 'rattail.telemetry'

    def load(self):

        keys = self._config_string('collect.keys')
        if not keys:
            keys = self._config_string('collect', ignore_ambiguous=True)
            if keys:
                warnings.warn(f"URGENT: instead of '{self.section}.{self.prefix}.collect', "
                              f"you should set '{self.section}.{self.prefix}.collect.keys'",
                              DeprecationWarning, stacklevel=2)
        self.collect_keys = self.config.parse_list(keys or 'os,postgresql,rattail,python')

        # nb. for now this is assumed to be `tailbone_api`
        #self.submit_type = self._config_string('submit')

        self.submit_url = self._config_string('submit.url')
        self.submit_uuid = self._config_string('submit.uuid')
