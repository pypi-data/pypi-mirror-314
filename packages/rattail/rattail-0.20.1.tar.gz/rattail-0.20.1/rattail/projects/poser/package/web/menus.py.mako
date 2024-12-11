## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} Menu
"""

from tailbone import menus as base


class ${studly_prefix}MenuHandler(base.MenuHandler):
    """
    ${name} menu handler
    """

    def make_menus(self, request, **kwargs):

        # TODO: override this if you need custom menus...

        # menus = [
        #     self.make_products_menu(request),
        #     self.make_admin_menu(request),
        # ]

        # ...but for now this uses default menus
        menus = super(${studly_prefix}MenuHandler, self).make_menus(request, **kwargs)

        return menus
