from datetime import datetime

class Dialog:
    def __init__(self, id=None, from_user=None, to_user=None, dialog=None):
        self._id = id
        self._from_user = from_user
        self._to_user = to_user
        self._dialog = dialog

    @property
    def id(self):
        return self._id or (self._dialog.id if self._dialog else None)

    @property
    def from_user(self):
        return self._from_user or (self._dialog.from_user if self._dialog else None)

    @property
    def to_user(self):
        return self._to_user or (self._dialog.to_user if self._dialog else None)

    def dict(self):
        return {
            "id": self.id,
            "from_user": self.from_user,
            "to_user": self.to_user
        }

class Message:
    def __init__(self, id=None, dialog_id=None ,from_user=None, message_=None):
        self._id = id
        self._dialog_id = dialog_id
        self._from_user = from_user
        self._message = message_

    @property
    def id(self):
        return self._id or (self._message.id if self._message else None)

    @property
    def dialog_id(self):
        return self._dialog_id or (self._message.dialog_id if self._message else None)

    @property
    def from_user(self):
        return self._from_user or (self._message.from_user if self._message else None)

    @property
    def message(self):
        return self._message or (self._message.message if self._message else None)


    def dict(self):
        return {
            "id": self.id,
            "dialog_id": self.dialog_id,
            "from_user": self.from_user,
            "message": self.message
        }
