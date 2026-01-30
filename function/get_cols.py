def get_cols(cur, target_table):
    query = f"""
    DESCRIBE {target_table}
    """
    cur.execute(query)

    cols = []
    for col in cur.fetchall():
        cols.append(col[0])

    return cols