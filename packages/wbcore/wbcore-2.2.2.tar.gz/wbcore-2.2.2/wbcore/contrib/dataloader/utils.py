def get_columns(cursor):
    return [col[0] for col in cursor.description or []]


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = get_columns(cursor)
    for row in cursor.fetchall():
        yield dict(zip(columns, row))


def dictfetchone(cursor):
    columns = get_columns(cursor)
    return dict(zip(columns, cursor.fetchone() or []))
