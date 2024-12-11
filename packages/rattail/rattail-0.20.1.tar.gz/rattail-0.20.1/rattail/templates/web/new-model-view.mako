## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Model View for ${model_title_plural}
"""

from ${model_module_name} import ${model_name}

from tailbone.views import MasterView


class ${view_class_name}(MasterView):
    """
    Master model view for ${model_title_plural}
    """
    model_class = ${model_name}

    route_prefix = '${route_prefix}'
    #permission_prefix = '${route_prefix}'

    #creatable = True
    #viewable = True
    #editable = True
    #deletable = False

    % if model_versioned:
    has_versions = True
    % endif

    grid_columns = [
        % for field in model_fieldnames:
        '${field}',
        % endfor
    ]

    form_fields = [
        % for field in model_fieldnames:
        '${field}',
        % endfor
    ]

    def configure_grid(self, g):
        super(${view_class_name}, self).configure_grid(g)

        # # name
        # g.filters['name'].default_active = True
        # g.filters['name'].default_verb = 'contains'
        # g.set_sort_defaults('name')
        # g.set_link('name')


def defaults(config, **kwargs):
    base = globals()

    ${view_class_name} = kwargs.get('${view_class_name}', base['${view_class_name}'])
    ${view_class_name}.defaults(config)


def includeme(config):
    defaults(config)
