#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterChassisDriver`
"""

import sys
import logging
import unittest

from shellfoundry.releasetools.test_helper import create_autoload_context_2g

from src.driver import IxiaChassis2GDriver

controller = ''
port = ''
address = '192.168.42.175'
address = '192.168.42.61'


class TestIxiaChassis2GDriver(unittest.TestCase):

    def setUp(self):
        self.context = create_autoload_context_2g(model='Ixia Chassis Shell 2G', address=address,
                                                  controller=controller, port=port, client_install_path='')
        self.driver = IxiaChassis2GDriver()
        self.driver.initialize(self.context)
        print self.driver.logger.handlers[0].baseFilename
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def tearDown(self):
        pass

    def testHelloWorld(self):
        pass

    def testAutoload(self):
        self.inventory = self.driver.get_inventory(self.context)
        for r in self.inventory.resources:
            print r.relative_address, r.model, r.name
        for a in self.inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    sys.exit(unittest.main())
