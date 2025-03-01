"""Configuring tests for the content suite
"""
from typing import Generator
from unittest import mock

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory, _mk_tmp

import demisto_sdk.commands.common.tools as tools
from TestSuite.integration import Integration
from TestSuite.json_based import JSONBased
from TestSuite.pack import Pack
from TestSuite.playbook import Playbook
from TestSuite.repo import Repo
from TestSuite.yml import YAML

# Helper Functions


def get_repo(request: FixtureRequest, tmp_path_factory: TempPathFactory) -> Repo:
    tmp_dir = _mk_tmp(request, tmp_path_factory)
    return Repo(tmp_dir)


def get_pack(request: FixtureRequest, tmp_path_factory: TempPathFactory) -> Pack:
    """Mocking tmp_path"""
    return get_repo(request, tmp_path_factory).create_pack()


def get_integration(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
) -> Integration:
    """Mocking tmp_path"""
    integration = get_pack(request, tmp_path_factory).create_integration()
    integration.create_default_integration()
    return integration


def get_playbook(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
) -> Playbook:
    """Mocking tmp_path"""
    playbook = get_pack(request, tmp_path_factory).create_playbook()
    playbook.create_default_playbook()
    return playbook


def get_script(request: FixtureRequest, tmp_path_factory: TempPathFactory):
    script = get_pack(request, tmp_path_factory).create_script()
    script.create_default_script()
    return script


# Fixtures


@pytest.fixture
def pack(request: FixtureRequest, tmp_path_factory: TempPathFactory) -> Pack:
    """Mocking tmp_path"""
    return get_pack(request, tmp_path_factory)


@pytest.fixture()
def script(request: FixtureRequest, tmp_path_factory: TempPathFactory):
    return get_script(request, tmp_path_factory)


@pytest.fixture
def integration(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
) -> Integration:
    """Mocking tmp_path"""
    return get_integration(request, tmp_path_factory)


@pytest.fixture
def repo(request: FixtureRequest, tmp_path_factory: TempPathFactory) -> Repo:
    """Mocking tmp_path"""
    return get_repo(request, tmp_path_factory)


@pytest.fixture(scope="module")
def module_repo(request: FixtureRequest, tmp_path_factory: TempPathFactory) -> Repo:
    from demisto_sdk.commands.find_dependencies.tests.find_dependencies_test import (
        working_repo,
    )

    return working_repo(get_repo(request, tmp_path_factory))


@pytest.fixture
def playbook(request: FixtureRequest, tmp_path_factory: TempPathFactory) -> Playbook:
    """Mocking tmp_path"""
    return get_playbook(request, tmp_path_factory)


@pytest.fixture()
def malformed_integration_yml(integration) -> YAML:
    """
    Provides an invalid integration yml structure.
    """
    integration.yml.write("1: 2\n//")
    return integration.yml


@pytest.fixture()
def malformed_incident_field(pack) -> JSONBased:
    """
    Provides an invalid incident field json structure.
    """
    incident_field = pack.create_incident_field("malformed")
    incident_field.write_as_text("{\n '1': '1'")
    return incident_field


@pytest.fixture(scope="session", autouse=True)
def mock_update_id_set_cpu_count() -> Generator:
    """
    Since Circle build has an issue in it's virtualization where it has only 2 vcpu's but the 'cpu_count' method returns
    all physical cpu's (36) it uses too many processes in the process pools.
    """
    with mock.patch(
        "demisto_sdk.commands.common.update_id_set.cpu_count", return_value=2
    ) as _fixture:
        yield _fixture


@pytest.fixture(autouse=True)
def clear_cache():
    tools.get_file.cache_clear()
