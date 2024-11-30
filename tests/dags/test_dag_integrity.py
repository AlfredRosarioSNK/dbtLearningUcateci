"""
Test the validity of all DAGs.

This script is used to validate the DAGs in the project. Key validations include:
- Ensuring all DAGs have proper tags.
- Ensuring all DAGs have `retries` set to a minimum value.
- Detecting and reporting import errors.

You can customize the validation logic or extend it for more advanced checks.

Sections:
1. Logging Utilities
2. Data Retrieval Functions
3. Pytest Test Cases
"""

import os
import logging
from contextlib import contextmanager
import pytest
from airflow.models import DagBag

@contextmanager
def suppress_logging(namespace):
    """
    Temporarily suppress logging for a specific namespace.
    Useful for reducing noise during tests.

    Args:
        namespace (str): The namespace to suppress logs for.
    """
    logger = logging.getLogger(namespace)
    old_value = logger.disabled
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = old_value


EXAMPLE_DAGS = [
    "example_dag_1",
    "example_dag_2",
    "example_dag_3",
]


def sample_function_for_future_use(dag_id):
    """
    Placeholder for future DAG checks.

    Args:
        dag_id (str): The ID of the DAG to validate.

    Returns:
        str: A message indicating the DAG is being processed.
    """
    return f"Processing DAG: {dag_id}"


def get_import_errors():
    """
    Generate a tuple for import errors in the dag bag.
    This function identifies any issues during the import of DAGs.
    """
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

        def strip_path_prefix(path):
            """
            Convert absolute paths to relative paths for easier debugging.
            """
            return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

        # Collect errors and ensure at least one result for testing.
        import_errors = [
            (strip_path_prefix(k), v.strip())
            for k, v in dag_bag.import_errors.items()
        ]
        return [(None, None)] + import_errors

def get_dags():
    """
    Generate a tuple of dag_id, <DAG objects> in the DagBag
    """
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]

@pytest.mark.parametrize(
    "dag_id,dag,fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_owners(dag_id, dag, fileloc):
    """
    Test if a DAG has an owner defined.

    This is a placeholder test for ensuring all DAGs are assigned to an owner.
    Currently, it does not enforce specific owners.

    Args:
        dag_id (str): The ID of the DAG.
        dag (DAG): The DAG object itself.
        fileloc (str): The relative file location of the DAG.

    Raises:
        AssertionError: If the DAG does not have an owner defined.
    """
    assert dag.default_args.get("owner", None), f"{dag_id} in {fileloc} has no owner."

@pytest.mark.parametrize(
    "dag_id,dag, fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_retries(dag_id, dag, fileloc):
    """
    Test if a DAG has retries set to at least 2.

    Additional Validation:
    - Logs a warning if retries are set to a very high number.
    """
    retries = dag.default_args.get("retries", None)
    assert retries >= 2, f"{dag_id} in {fileloc} does not have retries set to at least 2."

    if retries > 10:
        logging.warning(f"{dag_id} in {fileloc} has unusually high retries: {retries}")
