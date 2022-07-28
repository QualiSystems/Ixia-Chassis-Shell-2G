"""
Ixia chassis shell driver.
"""
import logging
from os import path

from cloudshell.logging.qs_logger import get_qs_logger
from cloudshell.shell.core.driver_context import AutoLoadDetails, InitCommandContext, ResourceCommandContext
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from ixexplorer.ixe_app import init_ixe
from ixexplorer.ixe_hw import IxeCard, IxeChassis, IxePort

from ixia_data_model import GenericTrafficGeneratorModule, GenericTrafficGeneratorPort, Ixia_Chassis_Shell_2G


class IxiaChassis2GDriver(ResourceDriverInterface):
    """Ixia chassis shell driver."""

    def __init__(self) -> None:
        """Initialize object variables, actual initialization is performed in initialize method."""
        self.logger: logging.Logger = None
        self.resource: Ixia_Chassis_Shell_2G = None

    def initialize(self, context: InitCommandContext) -> None:
        """Initialize Ixia chassis shell (from API)."""
        self.logger = get_qs_logger(log_group="traffic_shells", log_file_prefix=context.resource.name)
        self.logger.setLevel(logging.DEBUG)

    def cleanup(self) -> None:
        """Cleanup Ixia chassis shell (from API)."""
        super().cleanup()

    def get_inventory(self, context: ResourceCommandContext) -> AutoLoadDetails:
        """Load Ixia chassis inventory to CloudShell (from API)."""
        self.resource = Ixia_Chassis_Shell_2G.create_from_context(context)
        address = context.resource.address
        controller_address = self.resource.controller_address
        port = self.resource.controller_tcp_port

        if not controller_address:
            controller_address = address
        if not port:
            port = "4555"
        rsa_id = path.join(path.dirname(__file__), "id_rsa")

        ixia = init_ixe(self.logger, host=controller_address, port=int(port), rsa_id=rsa_id)
        ixia.connect()
        ixia.add(address)

        ixia.discover()
        self._load_chassis(list(ixia.chassis_chain.values())[0])
        return self.resource.create_autoload_details()

    def _load_chassis(self, chassis: IxeChassis) -> None:
        """Get chassis resource and attributes."""
        self.resource.model_name = chassis.typeName
        self.resource.vendor = "Ixia"
        self.resource.version = chassis.ixServerVersion

        for card_id, card in chassis.cards.items():
            self._load_module(card_id, card)

    def _load_module(self, card_id: int, card: IxeCard) -> None:
        """Get module resource and attributes."""
        gen_module = GenericTrafficGeneratorModule(f"Module{card_id}")
        self.resource.add_sub_resource(f"M{card_id}", gen_module)
        gen_module.model_name = card.typeName
        gen_module.serial_number = card.serialNumber.strip()
        gen_module.version = card.hwVersion

        for port_id, port in card.ports.items():
            self._load_port(gen_module, port_id, port)

    @staticmethod
    def _load_port(gen_module: GenericTrafficGeneratorPort, port_id: int, port: IxePort) -> None:
        """Get port resource and attributes."""
        gen_port = GenericTrafficGeneratorPort(f"Port{port_id}")
        gen_module.add_sub_resource(f"P{port_id}", gen_port)

        supported_speeds = port.supported_speeds()
        if not supported_speeds:
            supported_speeds = ["0"]
        gen_port.max_speed = int(max(supported_speeds, key=int))
        gen_port.configured_controllers = "IxLoad"
