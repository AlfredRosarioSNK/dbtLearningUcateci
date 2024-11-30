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

# Section 1: Logging Utilities
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
""