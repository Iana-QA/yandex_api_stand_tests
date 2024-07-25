import sender_stand_request
import data



def test_create_user_2_letter_in_first_name_get_success_response():
    # В переменную user_body сохраняется обновленное тело запроса с именем “Аа”
    user_body = sender_stand_request.get_user_body("Аа")
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)
    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1


def test_create_user_15_letter_in_first_name_get_success_response():
    user_body=sender_stand_request.get_user_body('Ааааааааааааааа')
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code==201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1


def test_negative_assert_symbol_create_user_1_letter_in_first_name():
    sender_stand_request.negative_assert_symbol('A')


def test_negative_assert_symbol_create_user_16_letter_in_first_name():
    sender_stand_request.negative_assert_symbol('Аааааааааааааааа')


def test_create_user_english_letter_in_first_name_get_success_response():
    sender_stand_request.positive_assert('QWErty')


def test_create_user_russia_letter_in_first_name_get_success_response():
    sender_stand_request.positive_assert('Мария')


def test_create_user_has_space_in_first_name_get_error_response():
    sender_stand_request.negative_assert_symbol('Человек и Ко')


def test_create_user_has_special_symbol_in_first_name_get_error_response():
    sender_stand_request.negative_assert_symbol('№%@')


def test_create_user_has_number_in_first_name_get_error_response():
    sender_stand_request.negative_assert_symbol('123')


def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    sender_stand_request.negative_assert_no_first_name(user_body)


def test_create_user_empty_first_name_get_error_response():
    user_body = sender_stand_request.get_user_body("")
    sender_stand_request.negative_assert_no_first_name(user_body)


def test_create_user_number_type_first_name_get_error_response():
    user_body = sender_stand_request.get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400




