import os
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

from line_notify import line_notify


def get_connect():
    db_path = os.getenv('DB_PATH')
    connect_string = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={db_path};'
    )
    return pyodbc.connect(connect_string)


def get_query():
    with open('insert.sql', mode='r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    load_dotenv()
    connect = get_connect()

    tsv_file = Path('SKN_RETURN.tsv', mode='r', encoding='cp932')

    with tsv_file.open() as f:
        for line in f:
            line = line.split('\t')
            renban, okm_zuban, process_symbol = line[11], line[13], line[6]
            query = get_query().format(renban, okm_zuban, process_symbol)
            cursor = connect.cursor()
            try:
                cursor.execute(query)
            except pyodbc.IntegrityError:
                pass
            else:
                connect.commit()

    cursor.close()
    connect.close()

    line_notify('Done')
