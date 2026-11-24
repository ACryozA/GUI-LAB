
SQL_MASTER_COLUMNS = ("type", "name", "tbl_name", "rootpage", "sql")

QUERY_TAB1 = "SELECT * FROM sqlite_master"
QUERY_TAB2 = "SELECT name FROM sqlite_master ORDER BY name"
QUERY_TAB4 = (
    "SELECT type AS object_type, COUNT(*) AS object_count "
    "FROM sqlite_master GROUP BY type ORDER BY type"
)
QUERY_TAB5 = (
    "SELECT name AS table_name, tbl_name, sql AS create_statement "
    "FROM sqlite_master "
    "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
)


def query_for_column(column: str) -> str:
    if column not in SQL_MASTER_COLUMNS:
        raise ValueError(f"Недопустимая колонка: {column}")
    return f'SELECT "{column}" FROM sqlite_master ORDER BY name'
