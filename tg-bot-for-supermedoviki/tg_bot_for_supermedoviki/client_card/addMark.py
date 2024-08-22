from PIL import Image
from random import randint


class AddMark:
    def __init__(self, user_id):
        self.user_id = user_id
        self.mark = Image.open("img/card_mark.png")
        self.random_angle = randint(-70, 70)  # Генерирует случайный угол от 0 до 360 градусов
        self.user_card = Image.open("result_card_12345.png")
        self.coffe_number = 7
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

    @staticmethod
    def generate(user_id):
        """Статический метод для добавления метки на фоновую картинку."""
        add_mark = AddMark(user_id)
        add_mark.rotate_mark()
        add_mark.position_mark()
        add_mark.add_mark()
        add_mark.user_card.save(f"result_card_{user_id}.png")


AddMark.generate(12345)