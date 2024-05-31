import pymssql
from config import config

def get_debt_user(user_id):
    try:
        with pymssql.connect(
                server=config.SERVER_NAME_MSSQL,
                port=config.PORT_MSSQL,
                user=config.USER_NAME_MSSQL,
                password=config.PASSWORD_MSSQL,
                database='A_Met_Book',
                as_dict=True
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM [A_Met_Book].[dbo].[LibraryDebtListForIIS_V2] where RDR_ID = '{user_id}'"
                           f" UNION ALL SELECT * FROM [A_Met_Book].[dbo].[LibraryNotDebtListForIIS] where RDR_ID = '{user_id}'")
            list_db = cursor.fetchall()

            for item in list_db:
                item['NAME'] = item['NAME'].encode('latin1').decode('cp1251')
                item['P_NAME'] = item['P_NAME'].encode('latin1').decode('cp1251')

            return list_db
    except Exception as e:
        print(e)