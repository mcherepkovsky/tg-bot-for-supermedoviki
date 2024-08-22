from typing import Any

from aiogram import types
from aiogram.filters import BaseFilter

from .. db.models import Users


class RoleFilter(BaseFilter):
    key = 'is_role'

    def __init__(self, role):  # Add an __init__ method to accept the role argument
        self.role = role  # Store the role for later use

    async def __call__(self, message: types.Message, **kwargs) -> str | bool | Any:
        user_id = message.from_user.id

        # Fetch user's position from the database
        try:
            employee = Users.get(Users.tg_id == user_id)
            position_title = employee.position_id.title  # Access position title
        except Users.DoesNotExist:
            position_title = "Guest"
            return position_title  # User not found in database

        # Check if the user's position matches the required role
        return position_title == self.role
