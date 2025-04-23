from sqlalchemy.future import select
from app.repository.models import MessageModel, DialogModel
from app.services.messages import Message
from app.services.users import User


class MessageRepository:
    def __init__(self, session):
        self.session = session

    async def add_dialog(self, dialog):
        self.session.add(dialog)
        # await self.session.flush()

    async def add(self, data):
        record = MessageModel(**data.dict())
        self.session.add(record)

    async def _get(self, id_):
        stmt = select(MessageModel).where(MessageModel.id == str(id_))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_message(self, message_id):
        message = await self._get(message_id)
        if message is not None:
            return Message(message_=message).dict()
        else:
            return None

    async def get_dialog_from_id(self, dialog_id):
        stmt = (
            select(DialogModel)
            .where(DialogModel.id == str(dialog_id))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_dialog(self, dialog):
        stmt = (
            select(DialogModel)
            .where(DialogModel.from_user == dialog.from_user)
            .where(DialogModel.to_user == dialog.to_user)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self,  dialog_id=None,  **filters):
        stmt = select(MessageModel).where(MessageModel.dialog_id == str(dialog_id))

        result = await self.session.execute(stmt)
        records = result.scalars().all()
        return [Message(**record.__dict__) for record in records]

    # async def update(self, id_, payload: dict):
    #     record = await self._get(id_)
    #     for key, value in payload.items():
    #         setattr(record, key, value)
    #     return User(user_=record)
    #
    # async def delete(self, id_):
    #     record = await self._get(id_)
    #     await self.session.delete(record)
