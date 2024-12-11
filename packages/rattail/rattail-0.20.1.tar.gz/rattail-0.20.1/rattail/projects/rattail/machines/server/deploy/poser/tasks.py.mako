## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-

from invoke import task


@task
def upgrade(ctx):
    ctx.run('/srv/envs/${env_name}/app/upgrade.sh --verbose')
