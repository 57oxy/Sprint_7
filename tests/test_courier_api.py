# Подключаем внешние модули и библиотеки
import allure
import pytest
from conftest import courier_fixture


@allure.epic('Тестирование API создания аккаунта курьера сервиса "Yandex Самокат"')
class TestAddCourierAPI:

    @allure.feature('Тестирование API создания аккаунта курьера')
    @allure.title('Проверка регистрации курьера с корректными данными')
    def test_create_courier_with_correct_credentials(self, courier_fixture):
        # Присваиваем переменной response тело созданного аккаунта
        response = courier_fixture.create_courier()
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title('Проверка регистрации курьера с повторяющимися данными')
    def test_create_with_repeated_credentials(self, courier_fixture):
        # Присваиваем переменной response тело созданного аккаунта создаем повторную учетку с теми же учетными данными что и в фикстуре
        response = courier_fixture.create_courier(courier_fixture.get_login(), courier_fixture.get_password(), courier_fixture.get_name())
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 409 and response.json().get('message') == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка невозможности регистрации курьера с пустыми логином или паролем')
    @pytest.mark.parametrize("key", ["login", "password"])
    def test_create_account_with_login_or_password_empty(self, courier_fixture, key):
        # Вызываем функцию создания курьера
        courier_fixture.create_courier()
        # Присваиваем переменной credentials информацию полученную при регистрации
        credentials = courier_fixture.get_account_data()
        # Опустошаем попеременно логин и пароль согласно параметризации
        credentials[key] = ''
        # Создаем курьера с имеющимися, но не полными данными для регистрации
        response = courier_fixture.create_courier(credentials)
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 400 and response.json().get('message') == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка регистрации курьера с пустым name')
    def test_create_account_with_no_name_positive(self, courier_fixture):
        # Вызываем функцию создания курьера
        courier_fixture.create_courier()
        # Присваиваем переменной credentials информацию полученную при регистрации
        credentials = courier_fixture.get_account_data()
        # Опустошаем имя курьера в переменной credentials
        credentials['name'] = ''
        # Создаем курьера с имеющимися, но не полными данными для регистрации
        response = courier_fixture.create_courier(credentials)
        # Проверяем что статус код и ответное сообщение корректные
        assert (response.status_code == 409 and response.json().get('message') == 'Этот логин уже используется. Попробуйте другой.')

@allure.epic('Тестирование API входа в аккаунт созданного курьера сервиса "Yandex Самокат"')
class TestLoginCourierAPI:

    @allure.feature('Тестирование API входа в аккаунт созданного курьера')
    @allure.title('Тестирование входа в аккаунт курьера с корректными данными')
    def test_login_courier_positive(self, courier_fixture):
        # Вызываем функцию входа курьера в аккаунт и получаем ответ от сервера
        response = courier_fixture.login_courier()
        # Получаем ID курьера
        courier_fixture.account_id = response.json().get('id')
        # Проверяем что статус код 200 и ID курьера не None
        assert response.status_code == 200 and courier_fixture.account_id is not None

    @allure.title('Тестирование входа в аккаунт курьера без обязательных полей логина или пароля')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_without_necessary_field_negative(self, courier_fixture, key):
        # Опустошаем попеременно логин и пароль в информации регистрации
        courier_fixture.data[key] = ''
        # Вызываем функцию входа курьера в аккаунт и получаем ответ от сервера
        response = courier_fixture.login_courier()
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 400 and response.json().get('message') == 'Недостаточно данных для входа'

    @allure.title('Тестирование входа в аккаунт курьера с неверными логина и пароля')
    @pytest.mark.parametrize("key", ("login", "password"))
    def test_login_with_wrong_credentials_negative(self, courier_fixture, key):
        # Присваиваем Unknown попеременно логин и пароль в информации регистрации
        courier_fixture.data[key] = 'Unknown'
        # Вызываем функцию входа курьера в аккаунт и получаем ответ от сервера
        response = courier_fixture.login_courier()
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 404 and response.json().get('message') == 'Учетная запись не найдена'


class TestDeleteCourierAPI:
    @allure.title('Тестирование удаления курьера с корректным id')
    def test_delete_courier_positive(self, courier_fixture):
        # Удаляем курьера, передаем ID курьера из функции
        response = courier_fixture.delete_courier(courier_fixture.get_courier_id())
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 200 and response.json() == {'ok': True}

    # БАГ - ожидаемый status_code в тесте должен быть - 400, всегда получаем 500, найден баг
    @allure.title('Тестирование удаления курьера с пустым id (Баг статуса - должен быть 400, а приходит 500 c соответствующим сообщением)')
    def test_delete_courier_with_empty_id_positive(self, courier_fixture):
        # Удаляем курьера, передаем ID курьера из функции
        response = courier_fixture.delete_courier(courier_fixture.get_courier_id())
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для удаления курьера'

    @allure.title('Тестирование удаления курьера с неверным id')
    def test_delete_courier_with_wrong_id_positive(self, courier_fixture):
        # Удаляем курьера, с ID 123 - ID такого курьера не существует
        response = courier_fixture.delete_courier(123)
        # Проверяем что статус код и ответное сообщение корректные
        assert response.status_code == 404
        assert response.json()['message'] == 'Курьера с таким id нет.'
