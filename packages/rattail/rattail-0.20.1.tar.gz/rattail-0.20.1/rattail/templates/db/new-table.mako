## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Table schema for ${model_title_plural}
"""

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db import model


class ${model_name}(model.Base):
    """
    ${description}
    """
    __tablename__ = '${table_name}'
    % if any([c['data_type']['type'] == '_fk_uuid_' for c in columns]):
    __table_args__ = (
        % for column in columns:
        % if column['data_type']['type'] == '_fk_uuid_':
        sa.ForeignKeyConstraint(['${column['name']}'], ['${column['data_type']['reference']}.uuid'],
                                name='${table_name}_fk_${column['data_type']['reference']}'),
        % endif
        % endfor
    )
    % endif
    % if versioned:
    % if all([c['versioned'] for c in columns]):
    __versioned__ = {}
    % else:
    __versioned__ = {
        'exclude': [
            % for column in columns:
            % if not column['versioned']:
            '${column['name']}',
            % endif
            % endfor
        ],
    }
    % endif
    % endif
    model_title = "${model_title}"
    model_title_plural = "${model_title_plural}"
    % for column in columns:

    % if column['name'] == 'uuid':
    uuid = model.uuid_column()
    % else:
    ${column['name']} = sa.Column(${column['formatted_data_type']}, nullable=${column['nullable']}, doc="""
    ${column['description'] or ''}
    """)
    % if column['data_type']['type'] == '_fk_uuid_' and column['relationship']:
    ${column['relationship']['name']} = orm.relationship(
        '${column['relationship']['reference_model']}',
        doc="""
        ${column['description'] or ''}
        """)
    % endif
    % endif
    % endfor

    # TODO: you usually should define the __str__() method

    # def __str__(self):
    #     return self.name or ""
