# Подключаем внешние модули и библиотеки
import pytest
from api.courier_api import CourierSamokatAPI


@pytest.fixture(scope='function')
def courier_fixture():
    # Инициализируем объект класса CourierSamokatAPI
    courier = CourierSamokatAPI()
    # Создаем учетку курьера
    courier.create_courier()
    # Передаем объект на данном этапе другим функциям
    yield courier
    # Удаляем курьера после тестов
    courier.delete_courier(courier.get_courier_id())

