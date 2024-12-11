## -*- mode: conf; -*-

include *.md
include *.rst

% if extends_db:
recursive-include ${pkg_name}/db/alembic *.py
recursive-include ${pkg_name}/db/alembic *.mako
% endif

% if has_web:
recursive-include ${pkg_name}/web/static *.css
recursive-include ${pkg_name}/web/static *.js
recursive-include ${pkg_name}/web/templates *.mako
% endif
