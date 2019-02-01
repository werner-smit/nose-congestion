from __future__ import absolute_import, print_function, unicode_literals

import time
import unittest
from nose.plugins import Plugin, PluginTester
import nose_congestion


class SmokeTests(PluginTester, unittest.TestCase):
    activate = '--with-congestion'
    congestion_plugin = nose_congestion.CongestionPlugin()
    plugins = [congestion_plugin]    

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

    def test_very_long_test_name_to_produce_name_that_is_longer_than_the_pre_defined_test_location_name_max_width(self):
        assert True

    def _generator(self, arg1):
        assert True


class SubSmokeTests(SmokeTests):
    def test_planet(self):
        assert True

class TestVeryLonGClassNameToExceedMaxLengthThisWouldHaveToBeVeryLongToDoThatAtThisPointItStillIsnt(PluginTester, unittest.TestCase):
    activate = '--with-congestion'
    plugins = [nose_congestion.CongestionPlugin()]    

    def setUp(self):
        time.sleep(0.05)

    def tearDown(self):
        time.sleep(0.07)

    def test_1(self):
        assert True
