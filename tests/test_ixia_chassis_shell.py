
"""
Tests for `IxiaChassisDriver`
"""

from cloudshell.api.cloudshell_api import ResourceAttributesUpdateRequest, AttributeNameValue, CloudShellAPISession

ixia_chassis = {
                'win-ixos': {'address': '192.168.42.61',
                             'controller': '',
                             'port': '',
                             'modules': 4,
                             },
                'lin-ixos': {'address': '192.168.42.217',
                             'controller': '',
                             'port': '8022',
                             'modules': 1,
                             },
                'win-ixos-no-defaults': {'address': '192.168.42.61',
                                         'controller': '192.168.42.61',
                                         'port': '4555',
                                         'modules': 4,
                                         },
                'lin-ixos-from-ixtcl-server': {'address': '192.168.42.217',
                                               'controller': 'localhost',
                                               'port': '',
                                               'modules': 1,
                                               },
                }


class TestIxiaChassis2GShell(object):

    session = None

    def setup(self):
        self.session = CloudShellAPISession('localhost', 'admin', 'admin', 'Global')

    def teardown(self):
        for resource in self.session.GetResourceList('Testing').Resources:
            self.session.DeleteResource(resource.Name)

    def test_hello_world(self):
        pass

    def test_win_ixos(self):
        self._get_inventory('win-ixos', ixia_chassis['win-ixos'])

    def test_lin_ixos(self):
        self._get_inventory('lin-ixos', ixia_chassis['lin-ixos'])

    def test_all(self):
        for key, value in ixia_chassis.items():
            self._get_inventory(key, value)

    def _get_inventory(self, name, properties):
        self.resource = self.session.CreateResource(resourceFamily='CS_TrafficGeneratorChassis',
                                                    resourceModel='Ixia Chassis Shell 2G',
                                                    resourceName=name,
                                                    resourceAddress=properties['address'],
                                                    folderFullPath='Testing',
                                                    parentResourceFullPath='',
                                                    resourceDescription='should be removed after test')
        self.session.UpdateResourceDriver(self.resource.Name, 'Ixia Chassis Shell 2G')
        attributes = [AttributeNameValue('Ixia Chassis Shell 2G.Controller Address', properties['controller']),
                      AttributeNameValue('Ixia Chassis Shell 2G.Controller TCP Port', properties['port']),
                      AttributeNameValue('Ixia Chassis Shell 2G.Client Install Path', '')]
        self.session.SetAttributesValues(ResourceAttributesUpdateRequest(self.resource.Name, attributes))
        self.session.AutoLoad(self.resource.Name)
        resource_details = self.session.GetResourceDetails(self.resource.Name)
        assert(len(resource_details.ChildResources) == properties['modules'])
        self.session.DeleteResource(self.resource.Name)
