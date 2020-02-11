
from os import path

from cloudshell.traffic.tg import TgChassisHandler

from ixexplorer.ixe_app import init_ixe

from ixia_data_model import Ixia_Chassis_Shell_2G, GenericTrafficGeneratorModule, GenericTrafficGeneratorPort


class IxiaHandler(TgChassisHandler):

    def initialize(self, context, logger):
        """
        :param InitCommandContext context:
        """
        resource = Ixia_Chassis_Shell_2G.create_from_context(context)
        super(self.__class__, self).initialize(resource, logger)

    def load_inventory(self, context):
        """
        :param InitCommandContext context:
        """

        address = context.resource.address
        controller_address = self.resource.controller_address
        port = self.resource.controller_tcp_port

        if not controller_address:
            controller_address = address
        if not port:
            port = '4555'
        rsa_id = path.join(path.dirname(__file__), 'id_rsa')

        self.ixia = init_ixe(self.logger, host=controller_address, port=int(port), rsa_id=rsa_id)
        self.ixia.connect()
        self.ixia.add(address)

        self.ixia.discover()
        self._load_chassis(self.ixia.chassis_chain.values()[0])
        return self.resource.create_autoload_details()

    def _load_chassis(self, chassis):
        """ Get chassis resource and attributes. """

        self.resource.model_name = chassis.typeName
        self.resource.vendor = 'Ixia'
        self.resource.version = chassis.ixServerVersion

        for card_id, card in chassis.cards.items():
            self._load_module(card_id, card)

    def _load_module(self, card_id, card):
        """ Get module resource and attributes. """

        gen_module = GenericTrafficGeneratorModule('Module{}'.format(card_id))
        self.resource.add_sub_resource('M{}'.format(card_id), gen_module)
        gen_module.model_name = card.typeName
        gen_module.serial_number = card.serialNumber.strip()
        gen_module.version = card.hwVersion

        for port_id, port in card.ports.items():
            self._load_port(gen_module, port_id, port)

    def _load_port(self, gen_module, port_id, port):
        """ Get port resource and attributes. """

        gen_port = GenericTrafficGeneratorPort('Port{}'.format(port_id))
        gen_module.add_sub_resource('P{}'.format(port_id), gen_port)

        supported_speeds = port.supported_speeds()
        if not supported_speeds:
            supported_speeds = ['0']
        gen_port.max_speed = int(max(supported_speeds, key=int))
        gen_port.configured_controllers='IxLoad'
