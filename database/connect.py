import mysql.connector
from config import config


def get_book(user_str):
    try:
        with mysql.connector.connect(
                user=config.USER_NAME_MYSQL,
                password=config.PASSWORD_MYSQL,
                host=config.HOST_NAME_MYSQL,
                database='mainlib',
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM `mainlib` WHERE name like '%{user_str}%' AND author!='-' ORDER BY year DESC;")
            result = cursor.fetchall()

            return result
    except Exception as e:
        print(e)