# Подключаем внешние модули и библиотеки
import allure
import requests
import helpers.constants as constants


class OrderSamokatAPI:

    def __init__(self):
        self.track_number = None
        self.id = None
        self.data = {}

    @allure.step('Создание заказа')
    def create_order(self, data):
        # Создаем POST запрос на создание заказа и присваиваем ответ переменной response
        response = requests.post(f"{constants.BASE_URL}{constants.CREATE_ORDER}", json=data)
        # Присваиваем переменной track_number номер заказа
        self.track_number = response.json()['track']
        # Присваиваем переменной data - информацию по заказу по трек номеру
        self.data = self.get_order_by_track_number(self.track_number)
        # Присваиваем переменной id - id заказа
        self.id = self.get_order_and_id_by_track_number(self.data)
        return response

    @allure.step('Получение списка заказов')
    def get_list_of_orders(self):
        # Возвращаем ответ на GET запрос со списком всех заказов
        return requests.get(constants.BASE_URL + constants.LIST_OF_ORDERS)

    @allure.step('Принятие заказа курьером')
    def accept_order(self, order_id, courier_id):
        # Возвращаем ответ на PUT запрос принятия заказа, в ручке передаем order_id и courier_id
        return requests.put(f"{constants.BASE_URL}{constants.ACCEPT_ORDER}/{order_id}?courierId={courier_id}", timeout=30)

    @allure.step('Получение заказа по номеру')
    def get_order_by_track_number(self, track_number):
        # Возвращаем ответ на GET запрос получения данных о заказе по track_number
        return requests.get(f"{constants.BASE_URL}{constants.GET_ORDER_BY_ID}?t={track_number}")

    @allure.step('Получение id заказа по номеру')
    def get_order_and_id_by_track_number(self, data):
        # Возвращаем часть информации из data
        return data.json()['order']['id']

    @allure.step('Получение id заказа')
    def get_order_id(self):
        # Возвращаем id заказа
        if self.id:
            return self.id
        return None

    @allure.step('Получить трек-номер заказа')
    def get_order_track_number(self):
        # Возвращаем трек номер заказа
        if self.track_number:
            return self.track_number
        return None
