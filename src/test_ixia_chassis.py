
"""
Tests for `IxiaChassis2GDriver`
"""

import time
import pytest

from cloudshell.api.cloudshell_api import AttributeNameValue
from cloudshell.traffic.tg import IXIA_CHASSIS_MODEL
from shellfoundry.releasetools.test_helper import (create_session_from_deployment, create_init_command_context,
                                                   create_autoload_resource)

from src.ixia_driver import IxiaChassis2GDriver


@pytest.fixture()
def model():
    yield IXIA_CHASSIS_MODEL


@pytest.fixture(params=[('192.168.65.32', '192.168.65.32', '8022'), ('192.168.42.61', '', '')],
                ids=['linux', 'windows'])
def dut(request):
    yield request.param


@pytest.fixture()
def session():
    yield create_session_from_deployment()


@pytest.fixture()
def context(session, model, dut):
    address, controller_address, controller_port = dut
    attributes = {model + '.Controller Address': controller_address,
                  model + '.Controller TCP Port': controller_port,
                  model + '.User': 'admin',
                  model + '.Password': 'DxTbqlSgAVPmrDLlHvJrsA=='}
    init_context = create_init_command_context(session, 'CS_TrafficGeneratorChassis', model, address, attributes,
                                               'Resource')
    yield init_context


@pytest.fixture()
def driver(context):
    driver = IxiaChassis2GDriver()
    driver.initialize(context)
    print(driver.logger.handlers[0].baseFilename)
    yield driver


@pytest.fixture()
def resource(session, model, dut):
    address, controller_address, controller_port = dut
    attributes = [
        AttributeNameValue(model + '.Controller Address', controller_address),
        AttributeNameValue(model + '.Controller TCP Port', controller_port),
        AttributeNameValue(model + '.User', 'admin'),
        AttributeNameValue(model + '.Password', 'admin')]
    resource = create_autoload_resource(session, 'CS_TrafficGeneratorChassis', model, address, 'test-ixia', attributes)
    time.sleep(2)
    yield resource
    session.DeleteResource(resource.Name)


def test_autoload(driver, context):
    inventory = driver.get_inventory(context)
    print('\n')
    for r in inventory.resources:
        print('{}, {}, {}'.format(r.relative_address, r.model, r.name))
    print('\n')
    for a in inventory.attributes:
        print('{}, {}, {}'.format(a.relative_address, a.attribute_name, a.attribute_value))


def test_autoload_session(session, resource):
    session.AutoLoad(resource.Name)
    session.GetResourceDetails(resource.Name)
