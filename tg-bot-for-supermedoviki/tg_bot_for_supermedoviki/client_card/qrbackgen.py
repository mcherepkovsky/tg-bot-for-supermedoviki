import io
import qrcode
from PIL import Image

class QRGen:
    def __init__(self, id):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        self.background = Image.open("tg_bot_for_supermedoviki/img/card.png")
        self.qr_img = None
        self.position = None
        self.id = id
        self.data = f"https://t.me/SupermedovikiBot?start={self.id}"

    @staticmethod
    def generate(id):
        """Статический метод для генерации QR-кода без создания экземпляра класса."""
        qr_gen = QRGen(id)
        qr_gen.create_qr()
        qr_gen.position_qr()
        qr_gen.paste_qr()
        return qr_gen.save_image()

    def create_qr(self):
        """Создает QR-код на основе данных."""
        self.qr.add_data(self.data)
        self.qr.make(fit=True)
        self.qr_img = self.qr.make_image(fill_color="#F4B136", back_color="#333333")
        self.qr_img = self.qr_img.resize((725, 725))

    def position_qr(self):
        """Определяет позицию для QR-кода на фоновой картинке."""
        self.position = (
            self.background.width // 4 - self.qr_img.width // 2 + 75,
            self.background.height // 2 - self.qr_img.height // 2,
        )

    def paste_qr(self):
        """Вставляет QR-код на фоновую картинку."""
        self.background.paste(self.qr_img, self.position)

    def save_image(self):
        """Сохраняет итоговое изображение как байты."""
        img_byte_arr = io.BytesIO()
        self.background.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
