# Подключаем внешние модули и библиотеки
import allure
import pytest
from conftest import courier_fixture
from api.order_api import OrderSamokatAPI
import helpers.helpers as helpers


@allure.epic('Тестирование API заказа самоката сервиса "Yandex Самокат"')
class TestOrderAPI:

    @allure.feature('Тестирование API создания заказа')
    @allure.title('Проверка создания заказа с корректными данными')
    @pytest.mark.parametrize('color', (['BLACK'], ['GREY'], ['BLACK', 'GREY'], ''))
    def test_create_order_with_correct_data(self, color):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа и присваиваем ее переменной
        order_data = helpers.generate_order_information(color)
        # Создаем заказ и получаем ответ
        response = order.create_order(order_data)
        # Проверяем что статус код 201 и track присутствует в ответе
        assert response.status_code == 201 and 'track' in response.json()

    @allure.title('Проверка получения списка заказов')
    def test_get_list_of_orders(self):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Получаем список заказов и записываем ответ
        response = order.get_list_of_orders()
        # Проверяем что статус код 200
        assert response.status_code == 200

    @allure.title('Проверка успешного принятия заказа курьером')
    def test_success_accept_order(self, courier_fixture):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Получаем order_id
        order_id = order.get_order_id()
        # Получаем courier_id
        courier_id = courier_fixture.get_courier_id()
        # Принимаем заказ используя order_id и courier_id
        response = order.accept_order(order_id, courier_id)
        # Проверяем что статус код 200 и ответ корректный
        assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.title('Проверка, что курьер не может принять заказ если заказ не существует')
    def test_accept_order_nonexistent_order_id_negative(self, courier_fixture):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа с черным самокатом и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Получаем courier_id
        courier_id = courier_fixture.get_courier_id()
        # Присваиваем номер заказа 000000
        order_id = 000000
        # Принимаем заказ используя order_id и courier_id
        response = order.accept_order(order_id=order_id, courier_id=courier_id)
        # Проверяем что статус код 404 и ответ корректный
        assert response.status_code == 404 and response.json()['message'] == "Заказа с таким id не существует"

    @allure.title('Проверка, что курьер, которого не существует не может принять заказ')
    def test_accept_order_nonexistent_courier_id_negative(self, courier_fixture):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа с черным самокатом и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Присваиваем id курьера 1234
        courier_id = 1234
        # Получаем order_id
        order_id = order.get_order_track_number()
        # Принимаем заказ используя order_id и courier_id
        response = order.accept_order(order_id, courier_id)
        # Проверяем что статус код 404 и ответ корректный
        assert response.status_code == 404 and response.json()['message'] == "Курьера с таким id не существует"

    # БАГ должен быть ответ 400, а появляется 404 с сообщением Not found
    @allure.title('Проверка, что курьер не может принять заказ с пустым номером заказа (БАГ должен быть ответ 400, а появляется 404 с сообщением Not found)')
    def test_accept_order_empty_order_id_negative(self, courier_fixture):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа с черным самокатом и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Получаем courier_id
        courier_id = courier_fixture.get_courier_id()
        # Присваиваем пустое значение переменной order_id
        order_id = ''
        # Принимаем заказ используя order_id и courier_id
        response = order.accept_order(order_id, courier_id)
        # Проверяем что статус код 400 и ответ корректный
        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для поиска"

    @allure.title('Проверка, что нельзя принять заказ с пустым id курьера')
    def test_accept_order_empty_courier_id_negative(self):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа с черным самокатом и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Присваиваем пустое значение переменной courier_id
        courier_id = ''
        # Получаем order_id
        order_id = order.get_order_id()
        # Принимаем заказ используя order_id и courier_id
        response = order.accept_order(order_id, courier_id)
        # Проверяем что статус код 400 и ответ корректный
        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для поиска"

    @allure.title('Проверка, что нельзя повторно принять заказ, который уже был в работе')
    def test_accept_order_had_been_in_progress_negative(self, courier_fixture):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа с черным самокатом и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Получаем courier_id
        courier_id = courier_fixture.get_courier_id()
        # Присваиваем переменной order_id значение 1 - данный заказ уже был в работе у другого курьера
        order_id = 1
        # Пытаемся принять заказ используя order_id и courier_id
        response = order.accept_order(order_id, courier_id)
        # Проверяем что статус код 409 и ответ корректный
        assert response.status_code == 409 and response.json()['message'] == "Этот заказ уже в работе"

    @allure.title('Проверка, что можно получить данные заказа по track number заказа')
    def test_get_order_by_track_positive(self):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Генерируем информацию для заказа с черным самокатом и присваиваем ее переменной
        order_data = helpers.generate_order_information(['BLACK'])
        # Создаем заказ и получаем ответ
        order.create_order(order_data)
        # Получаем track
        track = order.get_order_track_number()
        # Получаем данные заказа
        response = order.get_order_by_track_number(track)
        # Проверяем что статус код 200 и ответ корректный
        assert response.status_code == 200 and 'order' in response.json()

    @allure.title('Проверка, что нельзя получить данные заказа если номер заказа пустой')
    def test_get_order_with_no_id_negative(self):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Пытаемся получить данные заказа по пустому track номеру
        response = order.get_order_by_track_number('')
        # Проверяем что статус код 400 и ответ корректный
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для поиска'

    @allure.title('Проверка, что нельзя данные заказа если заказ не существует')
    def test_get_order_with_no_id_negative(self):
        # Инициализируем объект класса OrderSamokatAPI
        order = OrderSamokatAPI()
        # Пытаемся получить данные заказа по track номеру 1
        response = order.get_order_by_track_number(1)
        # Проверяем что статус код 404 и ответ корректный
        assert response.status_code == 404 and response.json()['message'] == 'Заказ не найден'
