# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
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
``rattail clonedb`` command
"""

import importlib
import logging
from typing import List

import typer
from typing_extensions import Annotated

from .base import rattail_typer


log = logging.getLogger(__name__)


@rattail_typer.command()
def clonedb(
        ctx: typer.Context,
        source_engine: Annotated[
            str,
            typer.Argument(help="SQLAlchemy engine URL for the source database.")] = ...,
        target_engine: Annotated[
            str,
            typer.Argument(help="SQLAlchemy engine URL for the target database.")] = ...,
        model: Annotated[
            str,
            typer.Option(help="Dotted path of Python module which contains the data model.")] = 'rattail.db.model',
        classes: Annotated[
            List[str],
            typer.Argument(help="Model classes which should be cloned.  Possible values here "
                           "depends on which module contains the data model.  If no classes "
                           "are specified, all available will be cloned.")] = None,
):
    """
    Clone (supported) data from a source DB to a target DB
    """
    from sqlalchemy import create_engine, orm

    config = ctx.parent.rattail_config
    app = config.get_app()
    progress = ctx.parent.rattail_progress
    model = importlib.import_module(model)
    assert classes

    source_engine = create_engine(source_engine)
    target_engine = create_engine(target_engine)
    model.Base.metadata.drop_all(bind=target_engine)
    model.Base.metadata.create_all(bind=target_engine)

    Session = orm.sessionmaker()
    src_session = Session(bind=source_engine)
    dst_session = Session(bind=target_engine)

    for clsname in classes:
        log.info("cloning data for model: %s", clsname)
        cls = getattr(model, clsname)
        src_query = src_session.query(cls)
        count = src_query.count()
        log.debug("found %d %s records to clone", count, clsname)
        if not count:
            continue

        mapper = orm.class_mapper(cls)
        key_query = src_session.query(*mapper.primary_key)

        def process(key, i):
            src_instance = src_query.get(key)
            dst_session.merge(src_instance)
            dst_session.flush()

        app.progress_loop(process, key_query, progress,
                          message=f"Cloning data for model: {clsname}")

    src_session.close()
    dst_session.commit()
    dst_session.close()
