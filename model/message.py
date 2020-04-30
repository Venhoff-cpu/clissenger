from model.entity import Entity
from model.user import User
from datetime import datetime


class Message(Entity):
    _id = None
    from_user = None
    to_user = None
    context = None
    created_at = None

    def __init__(self):
        self._id = -1
        self.from_user = User()
        self.to_user = User()
        self.context = ''
        self.created_at = datetime.now()

    @property
    def id(self):
        return self._id

    def save(self, cursor):
        if not self._id == -1:
            return False

        sql = """INSERT INTO messages(from_user, to_user, context, created_at)
                VALUES(%s, %s, %s, %s) RETURNING id"""
        values = (self.from_user, self.to_user, self.context, self.created_at)
        cursor.execute(sql, values)
        self._id = cursor.fetchone()[0]
        return True

    def update(self, cursor):
        if self._id == -1:
            return False

        sql = """UPDATE messeges SET context=%s WHERE id=%s"""
        values = (self.context, self.id)
        cursor.execute(sql, values)
        return True

    def delete(self, cursor):
        if self._id == -1:
            return False

        sql = "DELETE FROM messages WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

    def __str__(self):
        return f"From: {self.from_user}, To: {self.to_user}, message: {self.context}, on: {self.created_at}"