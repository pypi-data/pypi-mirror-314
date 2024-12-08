# -*- coding: utf-8; -*-
################################################################################
#
#  Wutta-Continuum -- SQLAlchemy Versioning for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
App Configuration
"""

import datetime
import socket

from sqlalchemy.orm import configure_mappers
from sqlalchemy_continuum import make_versioned
from sqlalchemy_continuum.plugins import Plugin

from wuttjamaican.conf import WuttaConfigExtension
from wuttjamaican.util import load_object


class WuttaContinuumConfigExtension(WuttaConfigExtension):
    """
    App :term:`config extension` for Wutta-Continuum.

    This adds a startup hook, which can optionally turn on the
    SQLAlchemy-Continuum versioning features for the main app DB.
    """
    key = 'wutta_continuum'

    def startup(self, config):
        """ """
        # only do this if config enables it
        if not config.get_bool('wutta_continuum.enable_versioning',
                               usedb=False, default=False):
            return

        # create wutta plugin, to assign user and ip address
        spec = config.get('wutta_continuum.wutta_plugin_spec',
                          usedb=False,
                          default='wutta_continuum.conf:WuttaContinuumPlugin')
        WuttaPlugin = load_object(spec)

        # tell sqlalchemy-continuum to do its thing
        make_versioned(plugins=[WuttaPlugin()])

        # nb. must load the model before configuring mappers
        app = config.get_app()
        model = app.model

        # tell sqlalchemy to do its thing
        configure_mappers()


class WuttaContinuumPlugin(Plugin):
    """
    SQLAlchemy-Continuum manager plugin for Wutta-Continuum.

    This tries to assign the current user and IP address to the
    transaction.

    It will assume the "current machine" IP address, which may be
    suitable for some apps but not all (e.g. web apps, where IP
    address should reflect an arbitrary client machine).

    However it does not actually have a way to determine the current
    user.  WuttaWeb therefore uses a different plugin, based on this
    one, to get both the user and IP address from current request.

    You can override this to use a custom plugin for this purpose; if
    so you must specify in your config file:

    .. code-block:: ini

       [wutta_continuum]
       wutta_plugin_spec = poser.db.continuum:PoserContinuumPlugin

    See also the SQLAlchemy-Continuum docs for
    :doc:`sqlalchemy-continuum:plugins`.
    """

    def get_remote_addr(self, uow, session):
        """ """
        host = socket.gethostname()
        return socket.gethostbyname(host)

    def get_user_id(self, uow, session):
        """ """

    def transaction_args(self, uow, session):
        """ """
        kwargs = {}

        remote_addr = self.get_remote_addr(uow, session)
        if remote_addr:
            kwargs['remote_addr'] = remote_addr

        user_id = self.get_user_id(uow, session)
        if user_id:
            kwargs['user_id'] = user_id

        return kwargs
