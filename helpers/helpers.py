# Подключаем внешние модули и библиотеки
import random
from faker import Faker


def generate_order_information(color):
    # Инициализируем объект класса
    fake = Faker()
    # Создаем массив и добавляем туда сгенерированные значения для заполнения полей
    order_body = {
        "name": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": fake.word(ext_word_list=['Бульвар Рокоссовского', 'Преображенская площадь', 'Октябрьская', 'Тургеневская', 'Третьяковская']),
        "phone": fake.phone_number(),
        "rentTime": random.randint(1, 5),  # between 1 and 7 days
        "deliveryDate": fake.date_between(start_date="today", end_date="+2y").strftime('%Y-%m-%d'),
        "comment": fake.sentence()
    }
    # Если цвет указан - добавляем цвет из параметра
    if color:
        order_body['color'] = color
    # Возвращаем массив для создания заказа
    return order_body
