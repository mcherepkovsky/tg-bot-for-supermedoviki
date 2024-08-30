import logging
from io import BytesIO
from random import randint
from typing import io

from PIL import Image


class AddMark:
    def __init__(self, user_id, coffe_number, user_card):
        self.user_id = user_id
        self.mark = Image.open("tg_bot_for_supermedoviki/resources/card_mark.png")
        self.random_angle = randint(-70, 70)  # Генерирует случайный угол от 0 до 360 градусов
        self.user_card = user_card
        self.coffe_number = coffe_number
        self.position = None

    def position_mark(self):
        """Определяет позицию для метки на фоновой картинке. (1325,655) старт, растояние 140"""
        if 4 > self.coffe_number > 0:
            self.position = (1325 + 140 * self.coffe_number, 655)
        elif 8 > self.coffe_number > 3:
            self.position = (1325 + 140 * (self.coffe_number - 4), 795)

    def rotate_mark(self):
        """Поворачивает метку на случайный угол."""
        self.mark = self.mark.rotate(self.random_angle, expand=True)

    def add_mark(self):
        """Добавляет метку на фоновую картинку."""
        self.user_card.paste(self.mark, self.position, self.mark)

    def save_image(self):
        """Сохраняет итоговое изображение как байты."""
        img_byte_arr = BytesIO()
        self.user_card.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    @staticmethod
    def generate(user_id, coffe_number, user_card):
        """Статический метод для добавления метки на фоновую картинку."""
        add_mark = AddMark(user_id, coffe_number, user_card)
        add_mark.rotate_mark()
        add_mark.position_mark()
        add_mark.add_mark()
        # add_mark.user_card.save(f"result_card_{user_id}.png")
        return add_mark.save_image()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# AddMark.generate(12345)
