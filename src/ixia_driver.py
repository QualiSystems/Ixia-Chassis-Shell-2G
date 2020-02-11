
from cloudshell.traffic.tg import TgChassisDriver

from ixia_handler import IxiaHandler


class IxiaChassis2GDriver(TgChassisDriver):

    def __init__(self):
        self.handler = IxiaHandler()

    def initialize(self, context):
        super(self.__class__, self).initialize(context)

    def cleanup(self):
        super(self.__class__, self).cleanup()

    def get_inventory(self, context):
        return super(self.__class__, self).get_inventory(context)
