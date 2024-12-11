include *.md
include *.rst
% if extends_db:
recursive-include ${pkg_name}/db/alembic *.py
% endif
