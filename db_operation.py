import os
from dotenv import load_dotenv
import datetime

import psycopg2

from services import reading_xlsx_file

load_dotenv('.env')  # загружаем данные из виртуального окружения

db_password = os.getenv('DATABASE_PASSWORD')
db_name = os.getenv('DATABASE_NAME')


def creating_table_kazaki():
    """ Создание в БД таблицы Казаки """

    connection = psycopg2.connect(user="postgres",
                                  password=db_password,
                                  host="127.0.0.1",
                                  port="5432",
                                  database=db_name)

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    # cursor.execute("""DROP TABLE IF EXISTS Kazaki""")

    # создаем таблицу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Kazaki (
        id SERIAL NOT NULL PRIMARY KEY,
        registry VARCHAR(50),
        account_number VARCHAR(15),
        name VARCHAR(100),
        ogrn VARCHAR(15),
        ogrn_date VARCHAR(15),
        address VARCHAR(100),
        form VARCHAR(50),
        region VARCHAR(100),
        status VARCHAR(20),
        status_date TIMESTAMP
        )
        ''')

    connection.commit()  # сохраняем изменения в БД

    cursor.close()  # закрываем курсор
    connection.close()  # закрываем соединение с БД


def filling_table_kazaki(companies_list):
    """ Заполнение в БД таблицы Казаки """

    connection = psycopg2.connect(user="postgres",
                                  password=db_password,
                                  host="127.0.0.1",
                                  port="5432",
                                  database=db_name)

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    # перебираем список полученных обществ
    for company in companies_list:

        # задаем данные для занесения в БД
        company_data = (
            company[0],  # реестр registry
            company[1],  # учетный номер account_number
            company[2],  # наименование name
            company[3],  # ОГРН ogrn
            company[4],  # дата ОГРН ogrn_date
            company[5],  # адрес address
            company[6],  # правовая форма form
            company[7],  # регион region
            company[8],  # статус status
            datetime.datetime.now()  # текущая дата
        )

        # проверяем существует ли общество в БД
        cursor.execute('SELECT * FROM Kazaki WHERE ogrn = %s', (company[3],))
        selected_company = cursor.fetchone()

        # если общество существует в БД
        if selected_company:

            # проверяем изменился ли статус общества
            if selected_company[9] != company[8]:  # если статус изменился

                # заносим обновленные данные
                cursor.execute("""UPDATE Kazaki SET status = %s, status_date = %s WHERE ogrn = %s""",
                               (company[8], datetime.datetime.now(), company[3],))

            print(selected_company)

        # если общества нет в БД, добавляем его
        else:
            cursor.execute("""INSERT INTO Kazaki (registry, account_number, name, ogrn, ogrn_date, address, 
            form, region, status, status_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", company_data)

            connection.commit()  # сохраняем изменения в БД

    # connection.commit()  # сохраняем изменения в БД

    cursor.close()  # закрываем курсор
    connection.close()  # закрываем соединение с БД


if __name__ == '__main__':

    creating_table_kazaki()

    society_list = reading_xlsx_file()

    filling_table_kazaki(society_list)
