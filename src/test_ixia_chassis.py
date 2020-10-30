
"""
Tests for `IxiaChassis2GDriver`
"""

from typing import List

import pytest

from cloudshell.api.cloudshell_api import AttributeNameValue, CloudShellAPISession, ResourceInfo
from cloudshell.shell.core.driver_context import AutoLoadCommandContext
from cloudshell.traffic.tg import TGN_CHASSIS_FAMILY, IXIA_CHASSIS_MODEL
from shellfoundry_traffic.test_helpers import (create_session_from_deployment, resource_init_command_context,
                                               create_autoload_resource, autoload_command_context, print_inventory)

from src.ixia_driver import IxiaChassis2GDriver


@pytest.fixture(params=[('192.168.65.30', '192.168.65.30', '8022'), ('192.168.65.30', 'localhost', '')],
                ids=['linux', 'windows'])
def dut(request):
    yield request.param


@pytest.fixture()
def session() -> CloudShellAPISession:
    yield create_session_from_deployment()


@pytest.fixture()
def autoload_context(session: CloudShellAPISession, dut: List[str]) -> AutoLoadCommandContext:
    address, controller_address, controller_port = dut
    # noinspection SpellCheckingInspection
    attributes = {f'{IXIA_CHASSIS_MODEL}.Controller Address': controller_address,
                  f'{IXIA_CHASSIS_MODEL}.Controller TCP Port': controller_port,
                  f'{IXIA_CHASSIS_MODEL}.User': 'admin',
                  f'{IXIA_CHASSIS_MODEL}.Password': 'DxTbqlSgAVPmrDLlHvJrsA=='}
    yield autoload_command_context(session, TGN_CHASSIS_FAMILY, IXIA_CHASSIS_MODEL, address, attributes)


@pytest.fixture()
def driver(session: CloudShellAPISession, dut: List[str]) -> IxiaChassis2GDriver:
    address, controller_address, controller_port = dut
    # noinspection SpellCheckingInspection
    attributes = {f'{IXIA_CHASSIS_MODEL}.Controller Address': controller_address,
                  f'{IXIA_CHASSIS_MODEL}.Controller TCP Port': controller_port,
                  f'{IXIA_CHASSIS_MODEL}.User': 'admin',
                  f'{IXIA_CHASSIS_MODEL}.Password': 'DxTbqlSgAVPmrDLlHvJrsA=='}
    init_context = resource_init_command_context(session, TGN_CHASSIS_FAMILY, IXIA_CHASSIS_MODEL, address, attributes,
                                                 'test-ixia')
    driver = IxiaChassis2GDriver()
    driver.initialize(init_context)
    print(driver.logger.handlers[0].baseFilename)
    yield driver


@pytest.fixture()
def autoload_resource(session: CloudShellAPISession, dut: List[str]) -> ResourceInfo:
    address, controller_address, controller_port = dut
    attributes = [AttributeNameValue(f'{IXIA_CHASSIS_MODEL}.Controller Address', controller_address),
                  AttributeNameValue(f'{IXIA_CHASSIS_MODEL}.Controller TCP Port', controller_port),
                  AttributeNameValue(f'{IXIA_CHASSIS_MODEL}.User', 'admin'),
                  AttributeNameValue(f'{IXIA_CHASSIS_MODEL}.Password', 'admin')]
    resource = create_autoload_resource(session, IXIA_CHASSIS_MODEL, 'test-ixia', address, attributes)
    yield resource
    session.DeleteResource(resource.Name)


def test_autoload(driver: IxiaChassis2GDriver, autoload_context: AutoLoadCommandContext) -> None:
    inventory = driver.get_inventory(autoload_context)
    print_inventory(inventory)


def test_autoload_session(session: CloudShellAPISession, autoload_resource: ResourceInfo, dut: List[str]) -> None:
    session.AutoLoad(autoload_resource.Name)
    resource_details = session.GetResourceDetails(autoload_resource.Name)
    assert len(resource_details.ChildResources) == 1
    assert resource_details.ChildResources[0].FullAddress == f'{dut[0]}/M1'
