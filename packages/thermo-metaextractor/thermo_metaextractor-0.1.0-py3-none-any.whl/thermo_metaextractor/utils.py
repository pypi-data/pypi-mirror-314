def read_query_from_file(file_path):
    """
    Reads an SQL query from a file.

    Args:
        file_path (str): Path to the SQL file.

    Returns:
        str: The SQL query as a string.
    """
    with open(file_path, 'r') as file:
        return file.read()
