## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} Views
"""


def includeme(config):

    # TODO: should use 'essential' views here

    # core views
    config.include('tailbone.views.common')
    config.include('tailbone.views.auth')
    config.include('tailbone.views.importing')
    config.include('tailbone.views.luigi')
    config.include('tailbone.views.menus')
    config.include('tailbone.views.tables')
    config.include('tailbone.views.upgrades')
    config.include('tailbone.views.progress')
    config.include('tailbone.views.views')

    # main table views
    config.include('tailbone.views.customergroups')
    config.include('tailbone.views.datasync')
    config.include('tailbone.views.email')
    config.include('tailbone.views.families')
    config.include('tailbone.views.members')
    config.include('tailbone.views.messages')
    config.include('tailbone.views.people')
    config.include('tailbone.views.reportcodes')
    config.include('tailbone.views.roles')
    config.include('tailbone.views.settings')
    config.include('tailbone.views.subdepartments')
    config.include('tailbone.views.shifts')
    config.include('tailbone.views.users')

    ## do we integrate w/ Catapult?
    % if integrates_catapult:
    config.include('tailbone_onager.views.stores')
    config.include('tailbone_onager.views.customers')
    config.include('tailbone_onager.views.employees')
    config.include('tailbone_onager.views.taxes')
    config.include('tailbone_onager.views.departments')
    config.include('tailbone_onager.views.brands')
    config.include('tailbone_onager.views.products')
    config.include('tailbone_onager.views.vendors')
    config.include('tailbone_onager.views.catapult')

    ## do we integrate w/ SMS?
    % elif integrates_locsms:
    config.include('tailbone.views.stores')
    config.include('tailbone.views.customers')
    config.include('tailbone.views.employees')
    config.include('tailbone.views.taxes')
    config.include('tailbone.views.departments')
    config.include('tailbone.views.brands')
    config.include('tailbone.views.vendors')
    config.include('tailbone.views.products')
    config.include('tailbone_locsms.views.locsms')

    ## no integration
    % else:
    config.include('tailbone.views.stores')
    config.include('tailbone.views.customers')
    config.include('tailbone.views.employees')
    config.include('tailbone.views.taxes')
    config.include('tailbone.views.departments')
    config.include('tailbone.views.brands')
    config.include('tailbone.views.vendors')
    config.include('tailbone.views.products')
    % endif

    # purchasing / receiving
    config.include('tailbone.views.purchases')
    config.include('tailbone.views.purchasing')

    # batch views
    config.include('tailbone.views.batch.handheld')
    config.include('tailbone.views.batch.inventory')
