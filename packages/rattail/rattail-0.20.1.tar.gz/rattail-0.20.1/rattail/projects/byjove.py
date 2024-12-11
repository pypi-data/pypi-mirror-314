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
Generator for 'byjove' projects
"""

import os

import colander

from rattail.projects import ProjectGenerator


class ByjoveProjectGenerator(ProjectGenerator):
    """
    Generator for Byjove app projects.
    """
    key = 'byjove'

    def make_schema(self, **kwargs):
        schema = colander.Schema()

        schema.add(colander.SchemaNode(name='system_name',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='name',
                                       typ=colander.String()))

        schema.add(colander.SchemaNode(name='slug',
                                       typ=colander.String()))

        return schema

    def generate_project(self, output, context, **kwargs):

        ##############################
        # root project dir
        ##############################

        self.generate('CHANGELOG.md.mako',
                      os.path.join(output, 'CHANGELOG.md'),
                      context)

        self.generate('gitignore',
                      os.path.join(output, '.gitignore'))

        self.generate('README.md.mako',
                      os.path.join(output, 'README.md'),
                      context)

        self.generate('vue.config.js.dist.mako',
                      os.path.join(output, 'vue.config.js.dist'),
                      context)

        self.generate('package.json.mako',
                      os.path.join(output, 'package.json'),
                      context)

        self.generate('tasks.py.mako',
                      os.path.join(output, 'tasks.py'),
                      context)

        ##############################
        # public
        ##############################

        public = os.path.join(output, 'public')
        os.makedirs(public)

        self.generate('public/index.html.mako',
                      os.path.join(public, 'index.html'),
                      context)

        self.generate('public/favicon.ico',
                      os.path.join(public, 'favicon.ico'))

        ##############################
        # src
        ##############################

        src = os.path.join(output, 'src')
        os.makedirs(src)

        self.generate('src/appsettings.js.dist.mako',
                      os.path.join(src, 'appsettings.js.dist'),
                      context)

        self.generate('src/appsettings.production.js.mako',
                      os.path.join(src, 'appsettings.production.js'),
                      context)

        self.generate('src/App.vue',
                      os.path.join(src, 'App.vue'))

        self.generate('src/main.js',
                      os.path.join(src, 'main.js'))

        self.generate('src/router.js',
                      os.path.join(src, 'router.js'))

        self.generate('src/store.js',
                      os.path.join(src, 'store.js'))

        ##############################
        # assets
        ##############################

        assets = os.path.join(src, 'assets')
        os.makedirs(assets)

        self.generate('src/assets/Hymenocephalus_italicus.jpg',
                      os.path.join(assets, 'Hymenocephalus_italicus.jpg'))

        ##############################
        # components
        ##############################

        components = os.path.join(src, 'components')
        os.makedirs(components)

        self.generate('src/components/AppNav.vue',
                      os.path.join(components, 'AppNav.vue'))

        ##############################
        # views
        ##############################

        views = os.path.join(src, 'views')
        os.makedirs(views)

        self.generate('src/views/Home.vue',
                      os.path.join(views, 'Home.vue'))

        self.generate('src/views/Login.vue',
                      os.path.join(views, 'Login.vue'))

        self.generate('src/views/About.vue',
                      os.path.join(views, 'About.vue'))

        ###############
        # customers
        ###############

        customers = os.path.join(views, 'customers')
        os.makedirs(customers)

        self.generate('src/views/customers/Customers.vue',
                      os.path.join(customers, 'Customers.vue'))

        self.generate('src/views/customers/Customer.vue',
                      os.path.join(customers, 'Customer.vue'))

        self.generate('src/views/customers/index.js',
                      os.path.join(customers, 'index.js'))

        ###############
        # products
        ###############

        products = os.path.join(views, 'products')
        os.makedirs(products)

        self.generate('src/views/products/Products.vue',
                      os.path.join(products, 'Products.vue'))

        self.generate('src/views/products/Product.vue',
                      os.path.join(products, 'Product.vue'))

        self.generate('src/views/products/index.js',
                      os.path.join(products, 'index.js'))
