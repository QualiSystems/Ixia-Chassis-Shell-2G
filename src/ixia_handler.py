
from os import path

from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute

from trafficgenerator.tgn_utils import ApiType
from ixexplorer.ixe_app import init_ixe


class IxiaHandler(object):

    def initialize(self, context, logger):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """

        self.logger = logger

        address = context.resource.address
        controller_address = context.resource.attributes['Ixia Chassis Shell 2G.Controller Address']
        port = context.resource.attributes['Ixia Chassis Shell 2G.Controller TCP Port']

        if not controller_address:
            controller_address = address
        if not port:
            port = '4555'
        rsa_id = path.join(path.dirname(__file__), 'id_rsa')

        self.ixia = init_ixe(ApiType.socket, self.logger, host=controller_address, port=int(port), rsa_id=rsa_id)
        self.ixia.connect()
        self.ixia.add(address)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.resources = []
        self.attributes = []
        self.ixia.discover()
        self._get_chassis_ixos(self.ixia.chassis_chain.values()[0])
        details = AutoLoadDetails(self.resources, self.attributes)
        return details

    def _get_chassis_ixos(self, chassis):
        """ Get chassis resource and attributes. """

        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Model Name',
                                                 attribute_value=chassis.typeName))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Ixia Chassis Shell 2G.Serial Number',
                                                 attribute_value=''))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Ixia Chassis Shell 2G.Server Description',
                                                 attribute_value=''))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Vendor',
                                                 attribute_value='Ixia'))
        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Version',
                                                 attribute_value=chassis.ixServerVersion))

        for card_id, card in chassis.cards.items():
            self._get_module_ixos(card_id, card)

    def _get_module_ixos(self, card_id, card):
        """ Get module resource and attributes. """

        relative_address = 'M' + str(card_id)
        model = 'Ixia Chassis Shell 2G.GenericTrafficGeneratorModule'
        resource = AutoLoadResource(model=model,
                                    name='Module' + str(card_id),
                                    relative_address=relative_address)
        self.resources.append(resource)
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorModule.Model Name',
                                                 attribute_value=card.typeName))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name=model + '.Serial Number',
                                                 attribute_value=card.serialNumber.strip()))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name=model + '.Version',
                                                 attribute_value=card.hwVersion))
        for port_id, port in card.ports.items():
            self._get_port_ixos(relative_address, port_id, port)

    def _get_port_ixos(self, card_relative_address, port_id, port):
        """ Get port resource and attributes. """

        relative_address = card_relative_address + '/P' + str(port_id)
        resource = AutoLoadResource(model='Ixia Chassis Shell 2G.GenericTrafficGeneratorPort',
                                    name='Port' + str(port_id),
                                    relative_address=relative_address)
        self.resources.append(resource)
        supported_speeds = port.supported_speeds() if port.supported_speeds() else ['0']
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorPort.Max Speed',
                                                 attribute_value=int(max(supported_speeds, key=int))))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorPort.Configured Controllers',
                                                 attribute_value='IxLoad'))
