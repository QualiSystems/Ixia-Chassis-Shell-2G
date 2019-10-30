
"""
Tests for `IxiaChassis2GDriver`
"""

import sys
import logging

from shellfoundry.releasetools.test_helper import create_autoload_context_2g, create_session_from_deployment

from src.driver import IxiaChassis2GDriver

controller = ''
port = '8022'
address = '192.168.65.32'

attributes = {'Ixia Chassis Shell 2G.Controller Address': controller,
              'Ixia Chassis Shell 2G.Controller TCP Port': port,
              'Ixia Chassis Shell 2G.User': 'admin',
              'Ixia Chassis Shell 2G.Password': 'DxTbqlSgAVPmrDLlHvJrsA=='}


class TestIxiaChassis2GDriver(object):

    def setup(self):
        self.session = create_session_from_deployment()
        self.context = create_autoload_context_2g(self.session, 'Ixia Chassis Shell 2G', address, attributes)
        self.driver = IxiaChassis2GDriver()
        self.driver.initialize(self.context)
        print(self.driver.logger.handlers[0].baseFilename)
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def teardown(self):
        pass

    def test_hello_world(self):
        pass

    def test_autoload(self):
        inventory = self.driver.get_inventory(self.context)
        print('\n')
        for r in inventory.resources:
            print('{}, {}, {}'.format(r.relative_address, r.model, r.name))
        print('\n')
        for a in inventory.attributes:
            print('{}, {}, {}'.format(a.relative_address, a.attribute_name, a.attribute_value))
