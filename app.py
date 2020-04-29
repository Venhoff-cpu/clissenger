import argparse

from model.user import User
from model.message import Message
from service.user_service import UserService
from service.message_service import MessageService
from utils.db import connect_to_db
from datetime import datetime


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--authorize', help='authorize user', action='store_true')
    parser.add_argument('-c', '--add-user', help='add custom user', action='store_true')
    parser.add_argument('-t', '--add-test-user', help='add test user', action='store_true')
    parser.add_argument('-l', '--list', help='list all users', action='store_true')
    parser.add_argument('-d', '--delete', help='remove selected user by username', action='store_true')
    parser.add_argument('-e', '--edit', help='update selected user by username', action='store_true')
    parser.add_argument('-u', '--username', help='user username')
    parser.add_argument('-p', '--password', help='user password')
    parser.add_argument('-n', '--new-password', help='user new password')
    parser.add_argument('-em', '--email', help='user email')
    parser.add_argument('-s', '--send', help='send message', action='store_true')
    parser.add_argument('-m', '--message', help='user message')
    parser.add_argument('-lm', '--list-msg', help='list all messages', action='store_true')
    parser.add_argument('-to', '--to-user', help='list all messages by recipient', action='store_true')
    parser.add_argument('-fr', '--from-user', help='list all messages by sender', action='store_true')
    parser.add_argument('-mi', '--msg-id', help='Find msg by id', action='store_true')
    args = parser.parse_args() # parse all arguments

    connection = connect_to_db()
    if connection is None:
        print('Cannot connect to database')
        exit(-1)

    cursor = connection.cursor()

    if args.authorize == True:
        is_user_logged = UserService.login(cursor, args.username, args.password)
        if is_user_logged == True:
            print('Authorization done')
        else:
            print('Username or password invalid')

    if args.add_user == True:
        user = User()
        user.username = args.username
        user.email = args.email
        user.set_password(args.password, 'testowa-sol')
        user.save(cursor)
        print('Your user is created')

    if args.add_test_user == True:
        user = User()
        user.username = 'test'
        user.email = 'test@test.pl'
        user.set_password('qwerty12', 'testowa-sol')
        user.save(cursor)
        print('User created')

    if args.list == True:
        print('List all users from database')
        users = UserService.get_all(cursor)
        for user in users:
            print(user)

    if args.list_msg == True:
        print("list of all messages:")
        msgs = MessageService.load_all_msg(cursor)
        for msg in msgs:
            print(msg)

    if args.from_user == True:
        print(f"Messages send from {args.from_user}")
        msgs = MessageService.load_all_messages_by_user(cursor, args.from_user)
        for msg in msgs:
            print(msg)

    if args.to_user == True:
        print(f"Messages send to {args.to_user}")
        msgs = MessageService.find_by_recipient(cursor, args.to_user)
        for msg in msgs:
            print(msg)

    if args.msg_id == True:
        print(f"Messages Id {args.msg_id}")
        msgs = MessageService.load_msg_by_id(cursor, args.msg_id)
        for msg in msgs:
            print(msg)

    if args.delete == True:
        user = UserService.find_by_username(cursor, args.username) # można uzupełnic o warunek z logowanie użytkownika
        if user is not None:
            is_user_logged = UserService.login(cursor, args.username, args.password)
            if is_user_logged == True:
                user.delete(cursor)
                print('User deleted')
            else:
                print('Username or password invalid')

    if args.edit == True:
        is_user_logged = UserService.login(cursor, args.username, args.password)
        # Check if username and password authorize user
        if is_user_logged == True:
            # If user logged then set new password from args.new_password
            user.set_password(args.new_password, 'testowa-sol')
            # user.update(cursor)
            user.update(cursor)
            print("Password updated")
        else:
            print('Username or password invalid')

    if args.send == True:
        user = UserService.find_by_username(cursor, args.username)
        if user is not None:
            is_user_logged = UserService.login(cursor, args.username, args.password)
            if is_user_logged == True:
                to_user = UserService.find_by_email(cursor, args.email)
                if to_user is not None:
                    context = args.message
                    if context:
                        msg = Message()
                        msg.from_user = user.id
                        msg.to_user = to_user.id
                        msg.context = args.message
                        msg.created_at = datetime.now()
                        msg.save(cursor)
                        print("Message send")
                    else:
                        print("No message provided")
                else:
                    print("No user with that email")

            else:
                print('Username or password invalid')
        else:
            print('Username or password invalid')

    cursor.close()
    connection.close()
