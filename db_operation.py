import os
from dotenv import load_dotenv

import psycopg2

load_dotenv('.env')  # загружаем данные из виртуального окружения

db_password = os.getenv('DATABASE_PASSWORD')
db_name = os.getenv('DATABASE_NAME')

connection = psycopg2.connect(user="postgres",
                              password=db_password,
                              host="127.0.0.1",
                              port="5432",
                              database=db_name)

# Курсор для выполнения операций с базой данных
cursor = connection.cursor()

cursor.close()
connection.close()
