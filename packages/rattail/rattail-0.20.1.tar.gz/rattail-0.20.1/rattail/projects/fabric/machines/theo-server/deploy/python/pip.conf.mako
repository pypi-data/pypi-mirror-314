## -*- mode: conf; -*-

[global]
extra-index-url =
    https://pypi.rattailproject.org/simple/
    % if integrates_with == 'catapult':
    https://<%text>${env.restricted_pypi_username}:${env.restricted_pypi_password}</%text>@pypi-restricted.rattailproject.org/catapult/
    % endif
log-file = <%text>${envroot}</%text>/pip.log
exists-action = i
