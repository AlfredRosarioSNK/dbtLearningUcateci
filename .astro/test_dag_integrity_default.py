"""
Test the validity of all DAGs. **USED BY DEV PARSE COMMAND DO NOT EDIT**
"""
from contextlib import contextmanager
import logging
import os

import pytest
from airflow.models import DagBag, Variable, Connection
from airflow.hooks.base import BaseHook
from airflow.utils.db import initdb

# Initialize the Airflow database
initdb()

# Patch for handling missing OS variables, Airflow Connections, and Variables during DAG parsing


# =========== MONKEYPATCH BaseHook.get_connection() ===========
def mock_get_connection(key: str, *args, **kwargs):
    print(f"Mocking Connection object for key: {key}")
    return Connection(key)


BaseHook.get_connection = mock_get_connection
# =========== /MONKEYPATCH BaseHook.get_connection() ===========


# =========== MONKEYPATCH os.getenv() ===========
def mock_getenv(key: str, *args, **kwargs):
    default = kwargs.get("default", args[0] if args else None)
    env_value = os.environ.get(key)

    if env_value:
        return env_value
    if key == "JENKINS_HOME" and default is None:
        return None
    return default or f"MOCKED_{key.upper()}_VALUE"


os.getenv = mock_getenv
# =========== /MONKEYPATCH os.getenv() ===========


# =========== MONKEYPATCH Variable.get() ===========
class MockedDict(dict):
    def __getitem__(self, key):
        return self.get(key, "MOCKED_KEY_VALUE")


def mock_variable_get(key: str, default_var=None, deserialize_json=False):
    print(f"Mocking Variable value for key: {key}")
    if default_var is not None:
        return default_var
    return MockedDict() if deserialize_json else "MOCKED_VARIABLE_VALUE"


Variable.get = mock_variable_get
# =========== /MONKEYPATCH Variable.get() ===========


@contextmanager
def suppress_logging(namespace):
    """
    Temporarily suppress logging for a specific namespace.
    """
    logger = logging.getLogger(namespace)
    original_state = logger.disabled
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = original_state


def get_import_errors():
    """
    Retrieve import errors from the DAG bag and format the results.
    """
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

        def format_path(path):
            return os.path.relpath(path, os.getenv("AIRFLOW_HOME"))

        return [(None, None)] + [
            (format_path(k), v.strip()) for k, v in dag_bag.import_errors.items()
        ]


@pytest.mark.parametrize(
    "rel_path,rv", get_import_errors(), ids=[x[0] for x in get_import_errors()]
)
def test_file_imports(rel_path, rv):
    """
    Ensure all DAG files can be imported without errors.
    """
    if rel_path and rv:
        raise Exception(f"{rel_path} failed to import with error:\n{rv}")
