from model.message import Message
from service.user_service import UserService
from service.password_service import check_password


class MessageService:
    # TODO: Create message service with methods:
    # - send_to_user(cursor, message, username)
    @staticmethod
    def sen_to_user(cursor, message, username):
        sql = "INSERT INTO messages(from_user, to_user, context) VALUES (%s, %s, %s)"
        # to_user = UserService.find_by_username(cursor, username)
        # cursor.execute(sql, (to_user.id, message,))

    # - get_all(cursor, username)
    @staticmethod
    def get_all_messages(cursor, username):
        sql = "SELECT id, from_user, to_user, context, created_at FROM messages WHERE from_user=%s"
        ret = []
        cursor.execute(sql, (username, ))
        data = cursor.fetchall()
        if data:
            for row in data:
                loaded_msg = Message()
                loaded_msg._id = data[0]
                loaded_msg.from_user = data[1]
                loaded_msg.to_user = data[2]
                loaded_msg.context = data[3]
                loaded_msg.created_at = data[4]
                ret.append(loaded_msg)
            return ret

    # - find_by_id(cursor, message_id)
    @staticmethod
    def load_msg_by_id(cursor, msg_id):
        sql = "SELECT id, from_user, to_user, context, created_at FROM messages WHERE id=%s"
        ret = []
        cursor.execute(sql, (msg_id,))
        data = cursor.fetchall()
        if data:
            for row in data:
                loaded_msg = Message()
                loaded_msg._id = data[0]
                loaded_msg.from_user = data[1]
                loaded_msg.to_user = data[2]
                loaded_msg.context = data[3]
                loaded_msg.created_at = data[4]
                ret.append(loaded_msg)
            return ret
        else:
            return None

    # - find_by_recipient(cursor, recipient_username)
    @staticmethod
    def find_by_recipient(cursor, recipient_username):
        sql = "SELECT id, from_user, to_user, context, created_at FROM messages WHERE to_user=%s"
        ret = []
        cursor.execute(sql, (recipient_username,))
        data = cursor.fetchall()
        if data:
            for row in data:
                loaded_msg = Message()
                loaded_msg._id = data[0]
                loaded_msg.from_user = data[1]
                loaded_msg.to_user = data[2]
                loaded_msg.context = data[3]
                loaded_msg.created_at = data[4]
                ret.append(loaded_msg)
            return ret
        else:
            return None
