"""
Tests for IxiaChassis2GDriver.
"""
# pylint: disable=redefined-outer-name
from typing import Iterable, List

import pytest
from _pytest.fixtures import SubRequest
from cloudshell.api.cloudshell_api import AttributeNameValue, CloudShellAPISession, ResourceInfo
from cloudshell.shell.core.driver_context import AutoLoadCommandContext
from cloudshell.traffic.tg import IXIA_CHASSIS_MODEL, TGN_CHASSIS_FAMILY
from shellfoundry_traffic.test_helpers import TgTestHelpers, print_inventory, session, test_helpers  # noqa: F401

from ixia_driver import IxiaChassis2GDriver


@pytest.fixture(params=[["192.168.65.26", "192.168.65.26", "8022"]], ids=["linux"])
def dut(request: SubRequest) -> list:
    """Yield Ixia device under test parameters."""
    return request.param


@pytest.fixture()
def autoload_context(test_helpers: TgTestHelpers, dut: List[str]) -> AutoLoadCommandContext:
    """Yield Ixia chassis shell command context for resource commands testing."""
    address, controller_address, controller_port = dut
    # noinspection SpellCheckingInspection
    attributes = {
        f"{IXIA_CHASSIS_MODEL}.Controller Address": controller_address,
        f"{IXIA_CHASSIS_MODEL}.Controller TCP Port": controller_port,
        f"{IXIA_CHASSIS_MODEL}.User": "admin",
        f"{IXIA_CHASSIS_MODEL}.Password": "DxTbqlSgAVPmrDLlHvJrsA==",
    }
    return test_helpers.autoload_command_context(TGN_CHASSIS_FAMILY, IXIA_CHASSIS_MODEL, address, attributes)


@pytest.fixture()
def driver(test_helpers: TgTestHelpers, dut: List[str]) -> Iterable[IxiaChassis2GDriver]:
    """Yield initialized IxiaChassis2GDriver."""
    address, controller_address, controller_port = dut
    # noinspection SpellCheckingInspection
    attributes = {
        f"{IXIA_CHASSIS_MODEL}.Controller Address": controller_address,
        f"{IXIA_CHASSIS_MODEL}.Controller TCP Port": controller_port,
        f"{IXIA_CHASSIS_MODEL}.User": "admin",
        f"{IXIA_CHASSIS_MODEL}.Password": "DxTbqlSgAVPmrDLlHvJrsA==",
    }
    init_context = test_helpers.resource_init_command_context(
        TGN_CHASSIS_FAMILY, IXIA_CHASSIS_MODEL, address, attributes, "test-ixia"
    )
    driver = IxiaChassis2GDriver()
    driver.initialize(init_context)
    yield driver
    driver.cleanup()


@pytest.fixture()
def autoload_resource(session: CloudShellAPISession, test_helpers: TgTestHelpers, dut: List[str]) -> Iterable[ResourceInfo]:
    """Yield Ixia chassis resource for shell autoload testing."""
    address, controller_address, controller_port = dut
    attributes = [
        AttributeNameValue(f"{IXIA_CHASSIS_MODEL}.Controller Address", controller_address),
        AttributeNameValue(f"{IXIA_CHASSIS_MODEL}.Controller TCP Port", controller_port),
        AttributeNameValue(f"{IXIA_CHASSIS_MODEL}.User", "admin"),
        AttributeNameValue(f"{IXIA_CHASSIS_MODEL}.Password", "admin"),
    ]
    resource = test_helpers.create_autoload_resource(IXIA_CHASSIS_MODEL, "tests/test-ixia", address, attributes)
    yield resource
    session.DeleteResource(resource.Name)


def test_autoload(driver: IxiaChassis2GDriver, autoload_context: AutoLoadCommandContext) -> None:
    """Test direct (driver) auto load command."""
    inventory = driver.get_inventory(autoload_context)
    print_inventory(inventory)


def test_autoload_session(session: CloudShellAPISession, autoload_resource: ResourceInfo, dut: List[str]) -> None:
    """Test indirect (shell) auto load command."""
    session.AutoLoad(autoload_resource.Name)
    resource_details = session.GetResourceDetails(autoload_resource.Name)
    assert len(resource_details.ChildResources) == 1
    assert resource_details.ChildResources[0].FullAddress == f"{dut[0]}/M1"
