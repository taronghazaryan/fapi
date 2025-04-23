from watchfiles import awatch

from app.exeptions import UserNotFoundError, UserAlreadyExistsError, PasswordMismatch
from app.repository.models import UserModel, DialogModel ,MessageModel


class MessageService:
    def __init__(self, message_repository):
        self.message_repository = message_repository

    async def create_dialog(self, dialog):
        new_dialog = DialogModel(**dialog.dict())
        await self.message_repository.add_dialog(new_dialog)
        return await self.get_dialog(dialog)

        # ////////this is gpt version, but this code dont work/////////
        #
        # await self.message_repository.add_dialog(new_dialog)
        # dialog_id = new_dialog.id  # он уже доступен после flush()
        # return dialog_id

    async def get_dialog(self, dialog):
        dialog_obj = await self.message_repository.get_dialog(dialog)
        return dialog_obj.id if dialog_obj else None

    async def get_dialog_from_id(self, dialog_id):
        dialog_obj = await self.message_repository.get_dialog_from_id(dialog_id)
        return dialog_obj

    async def create_message(self, data):
        message = MessageModel(
            dialog_id=data.dialog_id,
            from_user=data.from_user,
            message=data.message
        )

        await self.message_repository.add(message)
        return message

    async def get_message(self, message_id):
        message = await self.message_repository.get(message_id)
        if message is None:
            raise UserNotFoundError(f"Message with id:{message_id} not found.")
        return message


    # def update_user(self, user_id, data: dict):
    #     user = self.user_repository.get(user_id)
    #     if user is None:
    #         raise UserNotFoundError(f"User with id:{user_id} not found.")
    #     return self.user_repository.update(user_id, data)

    async def dialog_messages(self, dialog_id, **filters):
        messages_list = await self.message_repository.list(dialog_id=dialog_id, **filters)
        return messages_list
