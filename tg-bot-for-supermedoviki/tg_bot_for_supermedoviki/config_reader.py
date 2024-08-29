from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    # Желательно вместо str использовать SecretStr
    # для конфиденциальных данных, например, токена бота
    bot_token: SecretStr
    host: SecretStr
    user: SecretStr
    port: SecretStr
    database: SecretStr
    password: SecretStr

    # Начиная со второй версии pydantic, настройки класса настроек задаются
    # через model_config
    # В данном случае будет использоваться файла .env, который будет прочитан
    # с кодировкой UTF-8
    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8')


# При импорте файла сразу создастся
# и провалидируется объект конфига,
# который можно далее импортировать из разных мест
config = Settings()


# Чтение файла JSON с меню
with open('tg_bot_for_supermedoviki/resources/menu.json', 'r', encoding='utf-8') as file:
    menu_data = json.load(file)