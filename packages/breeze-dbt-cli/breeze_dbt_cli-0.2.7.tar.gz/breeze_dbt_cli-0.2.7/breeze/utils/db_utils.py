# breeze/utils/db_utils.py

from typing import List, Tuple
from breeze.utils.dbt_utils import get_profile, get_profile_name_from_dbt_project, get_target_from_profile

# Attempt to import database drivers
try:
    import pyodbc  # For SQL Server
except ImportError:
    pyodbc = None

try:
    import psycopg2  # For PostgreSQL and Redshift
except ImportError:
    psycopg2 = None

try:
    import snowflake.connector  # For Snowflake
except ImportError:
    snowflake = None

try:
    from google.cloud import bigquery  # For BigQuery
except ImportError:
    bigquery = None

def connect_to_sqlserver(target) -> 'pyodbc.Connection':
    if pyodbc is None:
        raise Exception("\u274c pyodbc is not installed. Please install it with 'pip install pyodbc'.")

    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={target.get('host')};"
            f"DATABASE={target.get('dbname')};"
            f"UID={target.get('user')};"
            f"PWD={target.get('password')}"
        )
        return conn
    except pyodbc.Error as e:
        raise Exception(f"Error connecting to SQL Server: {e}")

def connect_to_postgres(target) -> 'psycopg2.extensions.connection':
    if psycopg2 is None:
        raise Exception("\u274c psycopg2 is not installed. Please install it with 'pip install psycopg2-binary'.")

    try:
        conn = psycopg2.connect(
            dbname=target.get("dbname"),
            user=target.get("user"),
            password=target.get("password") or target.get("pass"),
            host=target.get("host"),
            port=target.get("port", 5432),
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"\u274c Error connecting to PostgreSQL: {e}")

def connect_to_snowflake(target) -> 'snowflake.connector.SnowflakeConnection':
    if snowflake is None:
        raise Exception("\u274c snowflake-connector-python is not installed. Please install it with 'pip install snowflake-connector-python'.")

    try:
        conn = snowflake.connector.connect(
            user=target.get("user"),
            password=target.get("password") or target.get("pass"),
            account=target.get("account"),
            database=target.get("database"),
            schema=target.get("schema"),
            role=target.get("role"),
            warehouse=target.get("warehouse"),
        )
        return conn
    except snowflake.connector.errors.ProgrammingError as e:
        raise Exception(f"\u274c Error connecting to Snowflake: {e}")

def connect_to_bigquery(target) -> 'bigquery.Client':
    if bigquery is None:
        raise Exception("\u274c google-cloud-bigquery is not installed. Please install it with 'pip install google-cloud-bigquery'.")

    try:
        client = bigquery.Client(project=target.get("project"))
        return client
    except Exception as e:
        raise Exception(f"\u274c Error connecting to BigQuery: {e}")

def get_columns_from_database(database: str, schema: str, identifier: str) -> List[Tuple[str, str]]:
    """
    Retrieve columns and their data types from the specified table.
    Returns a list of tuples: (column_name, data_type)
    """
    profile = get_profile()
    profile_name = get_profile_name_from_dbt_project()
    target = get_target_from_profile(profile, profile_name)
    db_type = target["type"]

    if not identifier:
        raise Exception("\u274c Could not determine the table name (identifier).")

    if db_type == "postgres":
        conn = connect_to_postgres(target)
        return get_columns_using_connection(conn, schema, identifier)
    elif db_type == "redshift":
        conn = connect_to_postgres(target)
        return get_columns_using_connection(conn, schema, identifier)
    elif db_type == "snowflake":
        conn = connect_to_snowflake(target)
        return get_columns_using_connection(conn, schema, identifier)
    elif db_type == "bigquery":
        client = connect_to_bigquery(target)
        return get_columns_bigquery(client, schema, identifier)
    elif db_type == "sqlserver":
        conn = connect_to_sqlserver(target)
        return get_columns_using_connection(conn, schema, identifier)
    else:
        raise Exception(f"\u274c Database type '{db_type}' is not supported.")

def get_columns_using_connection(conn, schema, identifier) -> List[Tuple[str, str]]:
    columns = []
    try:
        cursor = conn.cursor()
        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position;
        """
        cursor.execute(query, (schema, identifier))
        fetched_columns = cursor.fetchall()
        if not fetched_columns:
            raise Exception(
                f"\u274c Error: Table '{identifier}' does not exist in schema '{schema}'."
            )
        columns = [(row[0], row[1]) for row in fetched_columns]
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"\u274c Error querying database: {e}")
    return columns

def get_columns_bigquery(client, schema, identifier) -> List[Tuple[str, str]]:
    columns = []
    try:
        dataset_ref = client.dataset(schema)
        table_ref = dataset_ref.table(identifier)
        table = client.get_table(table_ref)
        if not table.schema:
            raise Exception(
                f"\u274c Error: Table '{identifier}' does not exist in schema '{schema}'."
            )
        columns = [(field.name, field.field_type.lower()) for field in table.schema]
    except Exception as e:
        raise Exception(f"\u274c Error querying BigQuery: {e}")
    return columns
