from __future__ import absolute_import, print_function, unicode_literals

import time
import unittest
from nose.plugins import Plugin, PluginTester
import nose_congestion


class SmokeTests(PluginTester, unittest.TestCase):
    activate = '--with-congestion'
    plugins = [nose_congestion.CongestionPlugin()]    

    def setUp(self):
        time.sleep(0.05)

    def tearDown(self):
        time.sleep(0.07)

    @classmethod
    def setup_class(cls):
        time.sleep(0.1)

    @classmethod
    def teardown_class(cls):
        time.sleep(0.15)

    def test_universe(self):
        assert True

    def test_multiverse(self):
        assert True
