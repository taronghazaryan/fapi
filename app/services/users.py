from datetime import datetime

class User:
    def __init__(self, id=None, first_name=None, last_name=None,
                 username=None, email=None, created=None, updated=None,
                 user_=None, verified=None, disabled=None):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._email = email
        self._disabled = disabled
        self._verified = verified
        self._created = created
        self._updated = updated
        self.user_ = user_

    @property
    def id(self):
        return self._id or (self.user_.id if self.user_ else None)

    @property
    def first_name(self):
        return self._first_name or (self.user_.first_name if self.user_ else None)

    @property
    def last_name(self):
        return self._last_name or (self.user_.last_name if self.user_ else None)

    @property
    def username(self):
        return self._username or (self.user_.username if self.user_ else None)

    @property
    def email(self):
        return self._email or (self.user_.email if self.user_ else None)

    @property
    def created(self):
        return self._created or (self.user_.created if self.user_ else None)

    @property
    def updated(self):
        return self._updated or (self.user_.updated if self.user_ else None)

    @property
    def verified(self):
        return self._verified or (self.user_.verified if self.user_ else None)

    @property
    def disabled(self):
        return self._disabled or (self.user_.disabled if self.user_ else None)


    def dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "verified": self.verified,
            "disabled": self.disabled,
        }
