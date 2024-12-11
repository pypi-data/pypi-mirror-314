## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
Product views for ${integration_name}
"""

from rattail_${integration_pkgname}.db.model import ${integration_studly_prefix}ProductCache

from tailbone.views import MasterView


class ${integration_studly_prefix}ProductCacheView(MasterView):
    """
    ${integration_name} Product views
    """
    model_class = ${integration_studly_prefix}ProductCache
    url_prefix = '/${integration_pkgname}/products'
    route_prefix = '${integration_pkgname}.products'
    creatable = False
    editable = False
    bulk_deletable = True
    has_versions = True

    labels = {
        '${integration_pkgname}_id': "${integration_name} ID",
    }

    grid_columns = [
        '${integration_pkgname}_id',
        'brand_name',
        'description',
        'price',
        'available',
    ]

    form_fields = [
        'product',
        '${integration_pkgname}_id',
        'brand_name',
        'description',
        'price',
        'available',
    ]

    def configure_grid(self, g):
        super(${integration_studly_prefix}ProductCacheView, self).configure_grid(g)

        g.filters['${integration_pkgname}_id'].default_active = True
        g.filters['${integration_pkgname}_id'].default_verb = 'equal'

        g.filters['description'].default_active = True
        g.filters['description'].default_verb = 'contains'

        g.filters['available'].default_active = True
        g.filters['available'].default_verb = 'is_true'

        g.set_sort_defaults('${integration_pkgname}_id')

        g.set_type('price', 'currency')

        g.set_link('${integration_pkgname}_id')
        g.set_link('description')

    def grid_extra_class(self, product, i):
        if product.available is False:
            return 'warning'

    def configure_form(self, f):
        super(${integration_studly_prefix}ProductCacheView, self).configure_form(f)

        f.set_renderer('product', self.render_product)

        f.set_type('price', 'currency')


def defaults(config, **kwargs):
    base = globals()

    ${integration_studly_prefix}ProductCacheView = kwargs.get('${integration_studly_prefix}ProductCacheView', base['${integration_studly_prefix}ProductCacheView'])
    ${integration_studly_prefix}ProductCacheView.defaults(config)


def includeme(config):
    defaults(config)
