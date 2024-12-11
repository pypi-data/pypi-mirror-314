## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} Views
"""

from tailbone.views import essentials


def includeme(config):

    essentials.defaults(config)

    # main table views
    config.include('tailbone.views.brands')
    config.include('tailbone.views.customergroups')
    config.include('tailbone.views.customers')
    config.include('tailbone.views.departments')
    config.include('tailbone.views.employees')
    config.include('tailbone.views.families')
    config.include('tailbone.views.members')
    config.include('tailbone.views.messages')
    config.include('tailbone.views.products')
    config.include('tailbone.views.reportcodes')
    config.include('tailbone.views.shifts')
    config.include('tailbone.views.stores')
    config.include('tailbone.views.subdepartments')
    config.include('tailbone.views.taxes')
    config.include('tailbone.views.vendors')

    # purchasing / receiving
    config.include('tailbone.views.purchases')
    config.include('tailbone.views.purchasing')

    # batch views
    config.include('tailbone.views.batch.handheld')
    config.include('tailbone.views.batch.inventory')
