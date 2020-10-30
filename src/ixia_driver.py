
from cloudshell.traffic.tg import TgChassisDriver

from ixia_handler import IxiaHandler


class IxiaChassis2GDriver(TgChassisDriver):

    def __init__(self):
        self.handler = IxiaHandler()

    def initialize(self, context):
        super().initialize(context)

    def cleanup(self):
        super().cleanup()

    def get_inventory(self, context):
        return super().get_inventory(context)
