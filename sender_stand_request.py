
import configuration
import requests
import data


def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body


def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)
# Вызов функции post_new_user с телом запроса для создания нового пользователя из модуля data
response = post_new_user(data.user_body);
# Вывод HTTP-статус кода ответа на запрос
# Код состояния указывает на результат обработки запроса сервером
print(response.status_code)
print(response.json())

def post_products_kits(body):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=body,
                         headers=data.headers)
response = post_products_kits(data.product_ids)
print(response.status_code)
print (response.json())

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)
response = get_users_table()
print(response.status_code)

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    response = post_new_user(user_body)
    assert response.status_code == 201
    assert response.json()['authToken'] != ''
    users_table_get = get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + response.json()["authToken"]
    assert users_table_get.text.count(str_user) == 1


def negative_assert_no_first_name(user_body):
    response = post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

