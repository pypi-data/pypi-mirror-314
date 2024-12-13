import re


def clean_table_name(full_table_name, schemas_to_remove):
    """
    Removes schema name if it matches the schemas_to_remove list.

    Args:
        full_table_name (str): The full table name including schema.
        schemas_to_remove (list): List of schemas to strip from table name.

    Returns:
        str: The cleaned table name without schema prefix if applicable.
    """
    parts = full_table_name.split('.')
    if len(parts) > 1 and parts[0].lower() in schemas_to_remove:
        return parts[-1]  # Return table name without schema
    return full_table_name  # Return as is if no schema or schema not in the list


def extract_table_names_and_data_sources(sql_query, schemas_to_remove):
    """
    Extracts table names and data source names from SQL query, cleaning up schema names.

    Args:
        sql_query (str): The SQL query.
        schemas_to_remove (list): List of schema names to remove.

    Returns:
        tuple: A tuple containing a list of cleaned table names and a list of data source names.
    """
    # Regular expression to capture tables after FROM or JOIN
    table_pattern = r'\b(?:from|join)\s+([a-zA-Z0-9_\.]+)'

    # Regular expression to capture data source names (e.g., database or server names in connection strings)
    data_source_pattern = r'Sql\.Database\(\"([^\"]+)\"\s*,\s*\"([^\"]+)\"'

    # Find all matching table names
    table_matches = re.findall(table_pattern, sql_query, re.IGNORECASE)
    cleaned_tables = [clean_table_name(match, schemas_to_remove) for match in table_matches]

    # Find all matching data source names
    data_source_matches = re.findall(data_source_pattern, sql_query)
    formatted_data_sources = [f"{server}, {database}" for server, database in data_source_matches]

    return sorted(set(cleaned_tables)), sorted(set(formatted_data_sources))


def extract_source_tables(sql_query, schemas_to_remove):
    """
    Extracts source tables mentioned in the SQL query.

    Args:
        sql_query (str): The SQL query.
        schemas_to_remove (list): List of schema names to remove.

    Returns:
        list: A list of cleaned source tables.
    """
    # Regular expression to capture tables after FROM or JOIN
    table_pattern = r'\b(?:from|join)\s+([a-zA-Z0-9_\.]+)'
    table_matches = re.findall(table_pattern, sql_query, re.IGNORECASE)
    cleaned_tables = [clean_table_name(match, schemas_to_remove) for match in table_matches]
    return sorted(set(cleaned_tables))
