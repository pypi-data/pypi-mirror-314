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
File monitor actions for creating batches
"""

import logging

from rattail.filemon import Action


log = logging.getLogger(__name__)


class MakeBatch(Action):
    """
    Filemon action for making new file-based batches.  Note that this only
    handles the simple case of creating a batch with a single input data file.
    """

    def __call__(self, path, batch_type='', handler='', user='',
                 delete_if_empty='false', auto_execute_allowed='true',
                 **kwargs):
        """
        Make a batch from the given file path.

        :param path: Path to the source data file for the batch.

        :param type: Type of batch, specified by the batch "key" - e.g. 'labels'.

        :param handler: Spec string for the batch handler class, e.g.
           ``'rattail.batch.handheld.handler:HandheldBatchHandler'``.  Note
           that this argument is *required*.

        :param user: Username of the user which is to be credited with creating
           the batch.

        :param delete_if_empty: Set this to 'true' if you wish the batch to be
           auto-deleted in the event that it has no data rows, after being
           initially populated from the given data file.

        :param auto_execute_allowed: Set this to 'false' if you wish to disable
           auto-execution of new batches.  Default behavior is for the handler
           to decide whether each batch is eligible for auto-execution.  Note
           that it is not possible to "force" auto-execution of a batch; you
           may only "allow" or "prevent" it.
        """
        if handler:
            handler = self.app.load_object(handler)(self.config)
        else:
            assert batch_type
            handler = self.app.get_batch_handler(batch_type)

        session = self.app.make_session()
        model = self.model

        user = session.query(model.User).filter_by(username=user).one()
        kwargs['created_by'] = user
        batch = handler.make_batch(session, **kwargs)
        handler.set_input_file(batch, path)
        handler.do_populate(batch, user)

        if self.config.parse_bool(delete_if_empty):
            session.flush()
            if not batch.data_rows:
                log.debug("auto-deleting empty '%s' batch: %s", handler.batch_key, batch)
                handler.do_delete(batch)
                batch = None

        if batch and self.config.parse_bool(auto_execute_allowed) and handler.auto_executable(batch):
            handler.execute(batch, user=user)
            batch.executed = self.app.make_utc()
            batch.executed_by = user

        session.commit()
        session.close()
