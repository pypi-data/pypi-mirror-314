import random

from datetime import datetime

from clickzetta import LoginParams, Client


def test_get_table_name_from_select():
    login_params = LoginParams("1", "Abc123456", "1")
    str_1 = '2023-02-05 13:23:44.675'
    print(str_1.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') + str(
        random.randint(10000, 99999)))
    print((datetime(2023, 3, 20) - datetime(1970, 1, 1)).days)
    date_string = "2023-03-20"
    date_time = datetime.strptime(date_string, '%Y-%m-%d')
    print((date_time - datetime(1970, 1, 1)).days)