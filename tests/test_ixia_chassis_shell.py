
"""
Tests for `IxiaChassis2GDriver`
"""

import pytest

from cloudshell.api.cloudshell_api import AttributeNameValue

from shellfoundry.releasetools.test_helper import create_session_from_deployment, create_autoload_resource_2g

chassis_properties = {'win-ixos': {'address': '192.168.42.61',
                                   'controller': '',
                                   'port': '',
                                   'modules': 4},
                      'lin-ixos': {'address': '192.168.65.32',
                                   'controller': '',
                                   'port': '8022',
                                   'modules': 1},
                      'lin-ixos-from-ixtcl-server': {'address': '192.168.65.32',
                                                     'controller': 'localhost',
                                                     'port': '',
                                                     'modules': 1}}


class TestIxiaChassis2GShell(object):

    session = None

    def setup(self):
        self.session = create_session_from_deployment()

    def teardown(self):
        self.session.DeleteResource(self.resource.Name)

    def test_hello_world(self):
        pass

    @pytest.mark.parametrize('chassis', ['win-ixos', 'lin-ixos-from-ixtcl-server'])
    def test_autoload(self, chassis):
        attributes = [
            AttributeNameValue('Ixia Chassis Shell 2G.Controller Address', chassis_properties[chassis]['controller']),
            AttributeNameValue('Ixia Chassis Shell 2G.Controller TCP Port', chassis_properties[chassis]['port'])]
        self.resource = create_autoload_resource_2g(self.session, 'Ixia Chassis Shell 2G',
                                                    chassis_properties[chassis]['address'], chassis, attributes)
        self.session.AutoLoad(self.resource.Name)
        resource_details = self.session.GetResourceDetails(self.resource.Name)
        assert(len(resource_details.ChildResources) == chassis_properties[chassis]['modules'])
