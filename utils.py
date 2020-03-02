from dbconfig import get_session
from orm import User

import string
import random
import hashlib


def create_user(username, password, first_name, last_name):
    salt = ''.join(random.sample(string.printable, 20))
    hash = hashlib.sha512()
    hash.update((password + salt).encode())
    salted_password = hash.hexdigest()

    session = get_session()

    session.add(User(
        username=username,
        firstname=first_name,
        lastname=last_name,
        password=salted_password,
        salt=salt
    ))

    session.commit()


def get_user(username, password):
    session = get_session()

    user = session.query(User).filter(User.username == username).one_or_none()

    if user is None:
        return None

    hash = hashlib.sha512()
    hash.update((password + user.salt).encode())

    return user if user.password == hash.hexdigest() else None
