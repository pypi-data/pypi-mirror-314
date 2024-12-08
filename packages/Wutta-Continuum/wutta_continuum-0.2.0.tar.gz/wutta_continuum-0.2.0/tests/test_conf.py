# -*- coding: utf-8; -*-

import socket

from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wutta_continuum import conf as mod


class TestWuttaContinuumConfigExtension(DataTestCase):

    def make_extension(self):
        return mod.WuttaContinuumConfigExtension()

    def test_startup(self):
        ext = self.make_extension()

        with patch.object(mod, 'make_versioned') as make_versioned:
            with patch.object(mod, 'configure_mappers') as configure_mappers:

                # nothing happens by default
                ext.startup(self.config)
                make_versioned.assert_not_called()
                configure_mappers.assert_not_called()

                # but will if we enable it in config
                self.config.setdefault('wutta_continuum.enable_versioning', 'true')
                ext.startup(self.config)
                make_versioned.assert_called_once()
                configure_mappers.assert_called_once_with()


class TestWuttaContinuumPlugin(DataTestCase):

    def make_plugin(self):
        return mod.WuttaContinuumPlugin()

    def test_remote_addr(self):
        plugin = self.make_plugin()
        with patch.object(socket, 'gethostbyname', return_value='127.0.0.1'):
            self.assertEqual(plugin.get_remote_addr(None, self.session), '127.0.0.1')

    def test_user_id(self):
        plugin = self.make_plugin()
        self.assertIsNone(plugin.get_user_id(None, self.session))

    def test_transaction_args(self):
        plugin = self.make_plugin()
        with patch.object(socket, 'gethostbyname', return_value='127.0.0.1'):
            self.assertEqual(plugin.transaction_args(None, self.session),
                             {'remote_addr': '127.0.0.1'})

            with patch.object(plugin, 'get_user_id', return_value='some-random-uuid'):
                self.assertEqual(plugin.transaction_args(None, self.session),
                                 {'remote_addr': '127.0.0.1',
                                  'user_id': 'some-random-uuid'})
