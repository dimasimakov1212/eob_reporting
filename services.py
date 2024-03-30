import requests
import datetime
import certifi
import urllib3
import os

urllib3.disable_warnings()


def get_data_xlsx():
    """
    Получение данных в формате xlsx
    :return:
    """

    url = 'https://reestrs.minjust.gov.ru/rest/registry/ac648356-fe24-e11a-ceb0-87718bb81ed4/export?'

    date_now = str(datetime.datetime.now().date())
    # print(date_now)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 '
                             'Safari/537.36'}

    response = requests.get(url, verify=False)
    # response = requests.get(url, headers=headers, timeout=5, verify=certifi.where())
    with open(f'./src/kazaki {date_now}.xlsx', 'wb') as output:
        output.write(response.content)
