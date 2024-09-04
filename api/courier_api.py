# Подключаем внешние модули и библиотеки
import allure
import requests
import random
import string
import helpers.constants as constants


class CourierSamokatAPI:

    def __init__(self):
        self.data = None
        self.account_id = None

    @allure.step('Создание тестовых данных пользователя')
    # Метод регистрации нового курьера возвращает список из логина, пароля и имени курьера
    def register_new_courier_and_return_data(self):
        # Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            # Создаем случайную строку
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for _ in range(length))
            return random_string
        # Генерируем логин, пароль и имя курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        name = generate_random_string(10)
        # Собираем тело запроса
        data = {
            "login": login,
            "password": password,
            "name": name,
        }
        return data

    @allure.step('Создание курьера')
    def create_courier(self, login='', password='', name=''):
        # Если логин пароль и имя пользователя пустые - генерируем новую случайную учетку курьера
        if login == '' and password == '' and name == '':
            self.data = self.register_new_courier_and_return_data()
        # Отправляем POST запрос на создание курьера со случайно сгенерированными данными
        return requests.post(f"{constants.BASE_URL}{constants.CREATE_COURIER}", json=self.data)

    @allure.step('Логин курьера')
    def login_courier(self,  login='', password=''):
        # Если логин и пароль пустые - создаем переменную data и вызываем функции get_login и get_password
        if login == '' and password == '':
            data = {
                "login": self.get_login(),
                "password": self.get_password(),
            }
        else:
            # В остальных случаях - используем логин и пароль из параметра
            data = {
                "login": login,
                "password": password
            }
        # Отправляем POST запрос на вход курьера в аккаунт используя логин и пароль полученный в начале функции
        return requests.post(f"{constants.BASE_URL}{constants.LOGIN_COURIER}", json=data)

    @allure.step('Получение логина зарегистрированного курьера')
    def get_login(self):
        # Возвращаем логин из информации полученной при регистрации курьера
        return self.data['login']

    @allure.step('Получение пароля зарегистрированного курьера')
    def get_password(self):
        # Возвращаем пароль из информации полученной при регистрации курьера
        return self.data['password']

    @allure.step('Получение имени зарегистрированного курьера')
    def get_name(self):
        # Возвращаем имя курьера из информации полученной при регистрации курьера
        return self.data['name']

    @allure.step('Получение всех данных зарегистрированного курьера (логин, пароль, имя)')
    def get_account_data(self):
        # Возвращаем всю информацию полученную при регистрации курьера
        return self.data

    @allure.step('Получение id курьера')
    def get_courier_id(self, login='', password=''):
        # Если логин и пароль пустые - создаем переменную data и вызываем функции get_login и get_password
        if login == '' and password == '':
            self.data = {
                "login": self.get_login(),
                "password": self.get_password(),
            }
        else:
            # В остальных случаях - используем логин и пароль из параметра
            self.data = {
                "login": login,
                "password": password
            }
        # Вызываем функцию login_courier с параметрами полученными из уже созданной случайной комбинации логина и пароля
        response = self.login_courier(self.get_login(), self.get_password())
        # Если код ответа 200 и ID курьера отсутствует - получаем его из ответа сервера и возвращаем ID курьера
        if response.status_code == 200 and self.account_id is None:
            self.account_id = response.json().get('id')
            return self.account_id

    @allure.step('Удаление курьера')
    def delete_courier(self, courier_id):
        # Отправляем запрос на удаление курьера, передаем ID курьера которого нужно удалить
        return requests.delete(f"{constants.BASE_URL}{constants.DELETE_COURIER}/{courier_id}")
