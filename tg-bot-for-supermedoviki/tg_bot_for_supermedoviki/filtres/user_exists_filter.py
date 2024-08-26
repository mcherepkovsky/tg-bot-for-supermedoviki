from aiogram.filters import BaseFilter
from aiogram.types import Message

from ..db.models import Users

USER_EXIST = lambda tg_id: Users.select().where(Users.tg_id == tg_id).exists()


class UserExist(BaseFilter):  # [1]
    def __init__(self, user_exist: bool):
        self.user_exist = user_exist

    async def __call__(self, message: Message) -> bool:  # [3]
        if self.user_exist:
            return bool(USER_EXIST(message.from_user.id))
        else:
            return not bool(USER_EXIST(message.from_user.id))
