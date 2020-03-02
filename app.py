from flask import Flask, request, g
from dbconfig import get_session

import functools

import utils

import orm

import uuid

import random
import string
import hashlib


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def use_sql_session(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        g.session = get_session()

        res = f(*args, **kwargs)

        g.session.commit()

        return res

    return wrapper


def authentication_only(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')

        if token is None:
            raise Exception('X-Auth-Token header is missing')

        g.token = g.session.query(orm.Token).filter(orm.Token.id == token).one_or_none()
        g.user = g.token.user

        if g.token is None:
            raise Exception('Token is invalid')

        return f(*args, **kwargs)

    return wrapper


@app.route('/login', methods=['POST'])
@use_sql_session
def login():
    r = request.get_json()
    user = utils.get_user(
        r['username'],
        r['password']
    )

    if user is None:
        return {
            'error': 'Access denied'
        }

    token_id = str(uuid.uuid4())
    g.session.add(orm.Token(
        id=token_id,
        userid=user.id
    ))

    return {'token': token_id}


@app.route('/logout', methods=['DELETE'])
@use_sql_session
@authentication_only
def logout():
    g.session.delete(g.token)

    return {}

@app.route('/users/', methods=['POST'])
@use_sql_session
@authentication_only
def users():
    r = request.get_json()
    r['username'], r['password']

    salt = ''.join(random.sample(string.printable, 20))
    hash = hashlib.sha512()
    hash.update((password + salt).encode())
    salted_password = hash.hexdigest()

    g.session.add(User(
        username=username,
        firstname=first_name,
        lastname=last_name,
        password=salted_password,
        salt=salt
    ))


@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
@use_sql_session
@authentication_only
def get_user(id):
    return g.session.query(User).filter(User.id == id).one_or_none()
     











