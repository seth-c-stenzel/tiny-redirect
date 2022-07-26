import sqlite3
from os.path import exists


def dict_factory(cursor, row):
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary


def load_settings(data):
    connection = sqlite3.connect("data.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    sql_query = "SELECT * FROM settings"

    cursor.execute(sql_query)
    data["settings"] = cursor.fetchone()
    connection.close()
    return data


def load_redirects(data):
    connection = sqlite3.connect("data.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    sql_query = "SELECT * FROM redirects"

    cursor.execute(sql_query)
    for redirect in cursor.fetchall():
        data["redirects"].update({redirect["alias"]: redirect["redirect"]})
    connection.close()
    return data


def load_data():
    data = {
        "settings": {},
        "redirects": {},
    }
    data = load_settings(data)
    data = load_redirects(data)
    return data


def add_alias(alias, redirect):
    connection = sqlite3.connect("data.db")
    add_sql = (
        f'INSERT INTO redirects ("alias", "redirect") VALUES ("{alias}", "{redirect}");'
    )
    try:
        cursor = connection.cursor()
        cursor.execute(add_sql)
        connection.commit()
    except sqlite3.OperationalError as error:
        connection.rollback()
        raise (error)
    finally:
        connection.close()


def delete_alias(alias):
    connection = sqlite3.connect("data.db")
    deletion_sql = f'DELETE FROM redirects WHERE "alias" == "{alias}";'
    try:
        cursor = connection.cursor()
        cursor.execute(deletion_sql)
        connection.commit()
    except sqlite3.OperationalError as error:
        connection.rollback()
        raise (error)
    finally:
        connection.close()


def update_setting(setting, current_value, new_value):
    connection = sqlite3.connect("data.db")
    update_sql = f'UPDATE settings SET "{setting}" = "{new_value}" WHERE "{setting}" == "{current_value}";'
    try:
        cursor = connection.cursor()
        cursor.execute(update_sql)
        connection.commit()
    except sqlite3.OperationalError as error:
        connection.rollback()
        raise (error)
    finally:
        connection.close()


def database_init():
    if not exists("data.db"):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE "settings" (
                "hostname"	TEXT DEFAULT '0.0.0.0' UNIQUE,
                "port"	INTEGER DEFAULT 80 UNIQUE,
                "shortname"	TEXT DEFAULT 'r' UNIQUE,
                "bottle-debug"	TEXT DEFAULT 'True' UNIQUE,
                "bottle-reloader"	TEXT DEFAULT 'True' UNIQUE,
                "bottle-engine"	TEXT DEFAULT 'wsgiref' UNIQUE,
                "theme"	TEXT DEFAULT 'Light' UNIQUE,
                "hide-console"	TEXT DEFAULT 'False' UNIQUE
            );
            """
        )

        cursor.execute('INSERT INTO settings (hostname) VALUES("0.0.0.0");')
        cursor.execute(
            """    
            CREATE TABLE "redirects" (
            "alias"	TEXT UNIQUE,
            "redirect"	TEXT
            );
            """
        )

        cursor.execute(
            'INSERT INTO redirects ("alias", "redirect") VALUES ("ex", "www.example.com");'
        )

        connection.commit()
        connection.close()
    return exists("data.db")


if __name__ == "__main__":
    from pprint import pprint as print

    data = load_data()
    print(data)
