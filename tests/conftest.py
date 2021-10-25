"""Provide fixtures to all test_*.py files."""

import argparse
import os

import pytest

from unittest import mock


@pytest.fixture(autouse=True)
def mock_environment_variables():  # noqa: D103
    # ensure external environment variables do not infer with tests,
    # and that the ones that are set by tfwrapper are cleared between tests
    path = os.environ["PATH"]
    with mock.patch.dict(os.environ, {"PATH": path}, clear=True):
        yield


@pytest.fixture
def default_args():  # noqa: D103
    parser = argparse.ArgumentParser()
    args = parser.parse_args([])
    args.confdir = "conf"
    args.account = None
    args.environment = None
    args.region = None
    args.stack = None
    return args


@pytest.fixture
def tmp_working_dir(tmp_path):  # noqa: D103
    # use path with more than 5 directories to avoid getting an unrelated conf dir outside tmp_path
    working_dir = tmp_path / "a" / "b" / "c" / "d" / "e"
    working_dir.mkdir(parents=True)
    os.chdir(working_dir)
    return {
        "working_dir": working_dir,
    }


@pytest.fixture
def tmp_working_dir_empty_conf(tmp_working_dir, default_args):  # noqa: D103
    paths = tmp_working_dir
    paths["conf_dir"] = paths["working_dir"] / default_args.confdir
    paths["conf_dir"].mkdir()
    paths["state_conf"] = paths["conf_dir"] / "state.yml"
    paths["wrapper_conf"] = paths["conf_dir"] / "config.yml"

    return paths


@pytest.fixture
def tmp_working_dir_regional(tmp_working_dir_empty_conf):  # noqa: D103
    paths = tmp_working_dir_empty_conf
    paths["account_dir"] = paths["working_dir"] / "testaccount"
    paths["environment_dir"] = paths["account_dir"] / "testenvironment"
    paths["region_dir"] = paths["environment_dir"] / "testregion"
    paths["stack_dir"] = paths["region_dir"] / "teststack"
    paths["stack_dir"].mkdir(parents=True)

    return paths


@pytest.fixture
def tmp_working_dir_global(tmp_working_dir_empty_conf):  # noqa: D103
    paths = tmp_working_dir_empty_conf
    paths["account_dir"] = paths["working_dir"] / "testaccount"
    paths["environment_dir"] = paths["account_dir"] / "_global"
    paths["stack_dir"] = paths["environment_dir"] / "teststack"
    paths["stack_dir"].mkdir(parents=True)

    return paths