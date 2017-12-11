
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell.traffic import tg_helper

from ixia_handler import IxiaHandler


class IxiaChassis2GDriver(ResourceDriverInterface):

    def __init__(self):
        self.handler = IxiaHandler()

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        self.logger = tg_helper.get_logger(context)
        self.handler.initialize(context, self.logger)

    def cleanup(self):
        pass

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self.handler.get_inventory(context)
