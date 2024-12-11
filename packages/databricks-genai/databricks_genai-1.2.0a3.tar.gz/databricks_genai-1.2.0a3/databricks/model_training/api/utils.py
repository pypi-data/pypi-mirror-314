"""Utility functions for the API."""

import hashlib
import logging
import os
from typing import Any, Callable, Tuple, cast

from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from IPython import get_ipython  # type: ignore
from pyspark.sql.session import SparkSession

logger = logging.getLogger(__name__)

_LOCAL_DEV_CONFIG_PROFILE = 'DBX_DEV_LOCAL'
_DATABRICKS_CONFIG_PROFILE_ENV = 'DATABRICKS_CONFIG_PROFILE'
_TEST_CONFIG_PROFILE = 'DBX_DEV_TEST'


def get_browser_url() -> str:
    w = WorkspaceClient()
    hostname = w.dbutils.notebook.entry_point.getDbutils().notebook().getContext().browserHostName().get()
    return f"https://{hostname}"


def get_spark() -> SparkSession:
    if is_running_in_databricks_notebook():
        # This is a hack - typing should be fine and hopefully will work better when in a notebook
        return cast(SparkSession, DatabricksSession.builder.getOrCreate())
    return SparkSession.builder.getOrCreate()


def is_running_in_databricks_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__  # pylint: disable = undefined-variable
        if shell == 'DatabricksShell':
            return True
        return False
    except Exception:  # pylint: disable = broad-except
        return False


def normalize_table_name(table_name: str) -> str:
    if table_name.startswith('`') and table_name.endswith('`'):
        return table_name

    table_name_parts = table_name.split('.')
    return '.'.join([f"`{part.strip('`')}`" if '-' in part else part for part in table_name_parts])


def get_schema_from_table(table_name: str) -> str:
    schema = table_name.replace('`', '').split('.')[:-1]
    return normalize_table_name('.'.join(schema))


def check_if_table_exists(table_name: str) -> bool:
    """Checks if the specified table already exists
    
    Args:
        table_name: The name of the table to validate.
    
    Returns:
        True if the table exists, False otherwise.
    """
    w = WorkspaceClient()
    r = w.tables.exists(normalize_table_name(table_name))
    return bool(r.table_exists)


def check_table_has_columns(table_name: str, columns: Tuple[str]) -> bool:

    spark = get_spark()
    df = spark.read.table(normalize_table_name(table_name))
    for column in columns:
        if column not in df.columns:
            return False
    return True


def get_display() -> Callable[[Any], None]:
    from IPython.display import display as default_display  # pylint: disable = import-outside-toplevel
    if is_running_in_databricks_notebook():
        # Get display from user namespace
        display = get_ipython().user_ns.get('display', default_display)
        return display
    else:
        return default_display


def get_me() -> str:
    """
    Get who is currently logged in.

    Returns:
        str: The name of the current user.
    """
    # TODO remove, only used for testing
    if os.environ.get(_DATABRICKS_CONFIG_PROFILE_ENV, '') in [
            _LOCAL_DEV_CONFIG_PROFILE,
            _TEST_CONFIG_PROFILE,
    ]:
        return 'me'

    w = WorkspaceClient()
    me = w.current_user.me().user_name or ''
    if not me:
        raise EnvironmentError('Could not determine the current user. Please check your environment.')
    logger.debug(f'You are {me}')
    return me


def get_workspace() -> int:
    """
    Get the current workspace id
    
    Returns:
        int: The workspace ID
    """
    w = WorkspaceClient()
    if is_running_in_databricks_notebook():
        ctx = w.dbutils.entry_point.getDbutils().notebook().getContext()
        return int(ctx.workspaceId().get())
    else:
        # not seeing this property on the object but it really does exist as far as I can tell
        return w.get_workspace_id()  # type: ignore


def get_host_and_token_from_env() -> Tuple[str, str]:
    """
    Get the host and token from the environment

    In a databricks notebook, the host will be the underlying region and env (i.e. oregon.staging.databricks.com)
    """
    if os.environ.get(_DATABRICKS_CONFIG_PROFILE_ENV, '') == _TEST_CONFIG_PROFILE:
        return 'test', 'test'
    w = WorkspaceClient()
    if is_running_in_databricks_notebook():
        ctx = w.dbutils.entry_point.getDbutils().notebook().getContext()
        host = ctx.apiUrl().get()
        token = ctx.apiToken().get()
    else:
        host = w.config.host
        token = w.config.token
    if not host or not token:
        raise EnvironmentError('Could not find root URL and/or token. Please check your environment.')
    return host, token


def get_cluster_id() -> str:
    """
    Get the cluster ID from the environment
    """
    if os.environ.get(_DATABRICKS_CONFIG_PROFILE_ENV, '') == _TEST_CONFIG_PROFILE:
        return 'test'
    w = WorkspaceClient()
    if is_running_in_databricks_notebook():
        ctx = w.dbutils.notebook.entry_point.getDbutils().notebook().getContext()
        cluster_id = ctx.clusterId().get()
    else:
        cluster_id = w.config.cluster_id
    return cluster_id


def md5_hash(s: str, num_digits=8) -> str:
    return hashlib.md5(s.encode()).hexdigest()[:num_digits]
