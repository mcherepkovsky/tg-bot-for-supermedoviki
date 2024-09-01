from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    bot_token: SecretStr
    host: SecretStr
    user: SecretStr
    port: SecretStr
    database: SecretStr
    password: SecretStr

    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8')


config = Settings()

# Чтение файла JSON с меню
with open('tg_bot_for_supermedoviki/resources/menu.json', 'r', encoding='utf-8') as file:
    menu_data = json.load(file)
